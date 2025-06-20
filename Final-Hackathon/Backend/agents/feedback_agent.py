import os
from state.state import PitchAnalysisState
from tools import generate_final_report_tool

def feedback_agent(state: PitchAnalysisState) -> PitchAnalysisState:
    print("🎯 Agent 5: Final Report Generation")
    
    try:
        report = generate_final_report_tool.invoke({
            "content_analysis": state["content_analysis"],
            "clarity_tone_analysis": state["clarity_tone_analysis"],
            "structure_analysis": state["structure_analysis"],
            "verbose": True
        })
        state["final_report"] = report
        state["current_agent"] = "completed"
        print("✅ Final report generated")

        audio_path = state.get("audio_path")
        if audio_path and os.path.exists(audio_path):
            os.remove(audio_path)
            print(f"🧹 Deleted audio file: {audio_path}")
    except Exception as e:
        state["error_message"] = str(e)
        state["current_agent"] = "error"
    
    return state
