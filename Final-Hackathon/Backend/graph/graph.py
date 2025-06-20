from langgraph.graph import StateGraph, START
from state.state import PitchAnalysisState
from agents.download_agent import download_agent,start_analysis
from agents.content_agent import content_agent
from agents.clarity_agent import clarity_agent
from agents.structure_agent import structure_agent
from agents.feedback_agent import feedback_agent
from agents.error_handler import error_handler
from agents.router import route_next_agent

def create_pitch_analysis_graph():
    """Create the LangGraph workflow"""
    
    workflow = StateGraph(PitchAnalysisState)
    
    # Add nodes
    workflow.add_node("start", start_analysis)
    workflow.add_node("download_agent", download_agent)
    workflow.add_node("content_agent", content_agent)
    workflow.add_node("clarity_agent", clarity_agent)
    workflow.add_node("structure_agent", structure_agent)
    workflow.add_node("feedback_agent", feedback_agent)
    workflow.add_node("error_handler", error_handler)
    
    # Add edges
    workflow.add_edge(START, "start")
    workflow.add_conditional_edges("start", route_next_agent)
    workflow.add_conditional_edges("download_agent", route_next_agent)
    workflow.add_conditional_edges("content_agent", route_next_agent)
    workflow.add_conditional_edges("clarity_agent", route_next_agent)
    workflow.add_conditional_edges("structure_agent", route_next_agent)
    workflow.add_conditional_edges("feedback_agent", route_next_agent)
    workflow.add_conditional_edges("error_handler", route_next_agent)
    
    return workflow.compile()