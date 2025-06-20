from state.state import PitchAnalysisState
from tools import clarity_tone_analysis_tool

def clarity_agent(state: PitchAnalysisState) -> PitchAnalysisState:
    print("🎤 Agent 3: Clarity & Tone Analysis")
    
    try:
        analysis = clarity_tone_analysis_tool.invoke({
            "transcript": state["transcript"],
            "audio_path": state["audio_path"],
            "audio_features": state["audio_features"],
            "verbose": True
        })
        state["clarity_tone_analysis"] = analysis
        state["current_agent"] = "structure_agent"
        print("✅ Clarity & tone analysis completed")
    except Exception as e:
        state["error_message"] = str(e)
        state["current_agent"] = "error"
    
    return state
