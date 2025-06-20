from state.state import PitchAnalysisState
from graph.graph import create_pitch_analysis_graph

def run_pitch_analysis(youtube_url: str) -> PitchAnalysisState:
    """Runs the full pitch analysis LangGraph pipeline"""

    app = create_pitch_analysis_graph()

    initial_state = PitchAnalysisState(
        youtube_url=youtube_url,
        transcript="",
        metadata={},
        audio_features={},
        audio_path="",
        content_analysis="",
        clarity_tone_analysis="",
        structure_analysis={},
        final_report={},
        current_agent="start",
        error_message="",
        retry_count=0
    )

    try:
        final_state = app.invoke(initial_state)
        return final_state
    except Exception as e:
        final_state["current_agent"] = "failed"
        final_state["error_message"] = str(e)
        return final_state
