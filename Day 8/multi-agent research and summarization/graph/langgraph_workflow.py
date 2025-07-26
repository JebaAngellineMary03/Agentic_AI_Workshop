from langgraph.graph import StateGraph, END
from agents.router_agent import route_query
from agents.web_research_agent import web_search_agent
from agents.rag_agent import rag_search_agent
from agents.summarization_agent import summarize_response
from typing import TypedDict, List

from langchain_core.runnables import RunnableLambda

# ✅ Step 1: Define the schema
class ResearchState(TypedDict):
    query: str
    route: str  # Add this
    intermediate_result: str  # Add this
    results: List[str]

def build_langgraph_workflow():
    # ✅ Step 2: Pass the schema here
    graph = StateGraph(ResearchState)

    # 1. Add all the nodes
    graph.add_node("router", RunnableLambda(route_query))

    graph.add_node("web_research", RunnableLambda(lambda s: {
        **s, "intermediate_result": web_search_agent(s["query"])
    }))

    graph.add_node("rag", RunnableLambda(lambda s: {
        **s, "intermediate_result": rag_search_agent(s["query"])
    }))

    graph.add_node("llm", RunnableLambda(lambda s: {
        **s, "intermediate_result": web_search_agent(s["query"])  # You can swap this later
    }))

    graph.add_node("summarize", RunnableLambda(summarize_response))

    # 2. Set entry and routing logic
    graph.set_entry_point("router")

    graph.add_conditional_edges("router", lambda state: state["route"], {
        "web_research": "web_research",
        "rag": "rag",
        "llm": "llm"
    })

    # 3. Add edges from the workers to summarization
    for node in ["web_research", "rag", "llm"]:
        graph.add_edge(node, "summarize")

    graph.add_edge("summarize", END)

    return graph.compile()
