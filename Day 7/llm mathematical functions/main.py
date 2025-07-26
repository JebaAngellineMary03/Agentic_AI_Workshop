import streamlit as st
from langchain_core.messages import HumanMessage
from agents.math_general_agent import build_agent

st.set_page_config(page_title="LangGraph Agent", layout="centered")
st.title("🧠 LangGraph General + Math Agent")

# Build the workflow once
try:
    workflow = build_agent()
    st.success("Workflow built successfully!")
except Exception as e:
    st.error(f"Error building workflow: {e}")
    st.stop()

# Initialize chat state
if "chat" not in st.session_state:
    st.session_state.chat = []

# Text input
user_input = st.text_input("Ask a question:")

if user_input:
    try:
        # Create initial state with the user message
        initial_state = {
            "messages": st.session_state.chat + [HumanMessage(content=user_input)]
        }
        
        # Invoke the workflow
        result = workflow.invoke(initial_state)
        
        # Check if result is valid and has messages
        if result and isinstance(result, dict) and "messages" in result:
            messages = result["messages"]
            if messages:
                # Update session state with all messages
                st.session_state.chat = messages
                
                # Display the latest response
                latest_message = messages[-1]
                if hasattr(latest_message, 'content'):
                    st.markdown(f"**Agent:** {latest_message.content}")
                else:
                    st.markdown("**Agent:** (Response has no content)")
            else:
                st.error("No messages in result")
        else:
            st.error("Invalid result from workflow")
            st.write(f"Result type: {type(result)}")
            st.write(f"Result: {result}")
            
    except Exception as e:
        st.error(f"Error: {str(e)}")
        import traceback
        st.code(traceback.format_exc())

# Display chat history
if st.session_state.chat:
    st.subheader("Chat History")
    for i, message in enumerate(st.session_state.chat):
        if hasattr(message, 'content'):
            message_type = type(message).__name__
            st.text(f"{i+1}. {message_type}: {message.content}")