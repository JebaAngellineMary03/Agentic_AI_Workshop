from state.state import PitchAnalysisState
from tools import structure_analysis_tool

def structure_agent(state: PitchAnalysisState) -> PitchAnalysisState:
    print("🏗️ Agent 4: Structure Analysis")
    
    try:
        analysis = structure_analysis_tool.invoke({
            "transcript": state["transcript"],
            "metadata": state["metadata"],
            "verbose": True
        })
        state["structure_analysis"] = analysis
        state["current_agent"] = "feedback_agent"
        print("✅ Structure analysis completed")
    except Exception as e:
        state["error_message"] = str(e)
        state["current_agent"] = "error"
    
    return state
