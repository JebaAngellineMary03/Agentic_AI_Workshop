from state.state import PitchAnalysisState

def route_next_agent(state: PitchAnalysisState) -> str:
    """Decide which agent should be invoked next."""
    return state.get("current_agent", "error_handler")
