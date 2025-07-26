from langgraph.graph import StateGraph, END
from langchain_core.messages import ToolMessage, AIMessage, HumanMessage
from tools.math_tools import plus, subtract, multiply, divide
from services.gemini_api import call_gemini
from typing import TypedDict, List

class AgentState(TypedDict):
    messages: List

def determine_route(state: AgentState):
    """Determine which node to route to based on the last message"""
    messages = state.get("messages", [])
    if not messages:
        return "llm"
    
    last_message = messages[-1]
    if not hasattr(last_message, 'content'):
        return "llm"
    
    msg = last_message.content.lower()
    
    # Extended math keywords and patterns
    math_keywords = [
        "plus", "add", "addition", "sum",
        "subtract", "minus", "subtraction", "difference", 
        "multiply", "times", "multiplication", "product",
        "divide", "division", "quotient",
        "calculate", "compute", "what is", "what's"
    ]
    
    math_symbols = ["+", "-", "*", "/", "×", "÷"]
    
    # Check for math keywords
    has_math_keyword = any(keyword in msg for keyword in math_keywords)
    
    # Check for math symbols
    has_math_symbol = any(symbol in msg for symbol in math_symbols)
    
    # Check for number patterns (like "7 times 8", "5 plus 3")
    import re
    has_numbers = bool(re.search(r'\d+', msg))
    
    # Route to math if it has math indicators and numbers
    if (has_math_keyword or has_math_symbol) and has_numbers:
        return "math"
    else:
        return "llm"

def math_node(state: AgentState):
    """Process mathematical operations"""
    messages = state.get("messages", [])
    
    if not messages:
        messages = []
        state["messages"] = messages
        messages.append(ToolMessage(content="No message to process", tool_call_id="math"))
        return state
    
    msg = messages[-1].content.lower()
    words = msg.split()
    
    try:
        # Extract numbers from the message using regex
        import re
        
        # Find all numbers in the message (including those in expressions like "5+5")
        number_pattern = r'\d+(?:\.\d+)?'
        number_matches = re.findall(number_pattern, msg)
        nums = [float(num) for num in number_matches]
        
        if len(nums) < 2:
            result = f"I found {len(nums)} number(s): {nums}. Please provide two numbers for the calculation."
        elif any(op in msg for op in ["plus", "add"]) or "+" in msg:
            result = f"{nums[0]} + {nums[1]} = {plus.invoke({'a': nums[0], 'b': nums[1]})}"
        elif any(op in msg for op in ["subtract", "minus", "difference"]) or "-" in msg:
            result = f"{nums[0]} - {nums[1]} = {subtract.invoke({'a': nums[0], 'b': nums[1]})}"
        elif any(op in msg for op in ["multiply", "times", "product"]) or "*" in msg or "×" in msg:
            result = f"{nums[0]} × {nums[1]} = {multiply.invoke({'a': nums[0], 'b': nums[1]})}"
        elif any(op in msg for op in ["divide", "division", "quotient"]) or "/" in msg or "÷" in msg:
            div_result = divide.invoke({'a': nums[0], 'b': nums[1]})
            result = f"{nums[0]} ÷ {nums[1]} = {div_result}"
        else:
            result = "I can help with addition (+, plus, add), subtraction (-, minus, subtract), multiplication (*, multiply), and division (/, divide)."
            
    except Exception as e:
        result = f"Error processing math operation: {str(e)}"
    
    # Add the result as a tool message
    messages.append(ToolMessage(content=result, tool_call_id="math"))
    state["messages"] = messages
    return state

def llm_node(state: AgentState):
    """Process general queries using LLM"""
    messages = state.get("messages", [])
    
    if not messages:
        messages = []
        state["messages"] = messages
        ai_response = AIMessage(content="Hello! How can I help you today?")
    else:
        msg = messages[-1].content
        try:
            ai_response = call_gemini(msg)
            
            # Ensure the response is an AIMessage
            if not isinstance(ai_response, AIMessage):
                ai_response = AIMessage(content=str(ai_response))
        except Exception as e:
            ai_response = AIMessage(content=f"Sorry, I encountered an error: {str(e)}")
    
    messages.append(ai_response)
    state["messages"] = messages
    return state

def build_agent():
    """Build the LangGraph workflow"""
    # Create the state graph
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("math", math_node)
    workflow.add_node("llm", llm_node)
    
    # Add conditional edges based on the routing function
    workflow.add_conditional_edges(
        "math",
        lambda x: END,  # Math node always goes to END
        {END: END}
    )
    
    workflow.add_conditional_edges(
        "llm", 
        lambda x: END,  # LLM node always goes to END
        {END: END}
    )
    
    # Set conditional entry point
    workflow.add_conditional_edges(
        "__start__",
        determine_route,
        {
            "math": "math",
            "llm": "llm"
        }
    )
    
    return workflow.compile()