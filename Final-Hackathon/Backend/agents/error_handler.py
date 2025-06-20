from state.state import PitchAnalysisState

def error_handler(state: PitchAnalysisState) -> PitchAnalysisState:
    print(f"❌ Error in {state.get('current_agent', 'unknown')}: {state.get('error_message', 'Unknown error')}")
    
    if state.get("retry_count", 0) < 2:
        state["retry_count"] = state.get("retry_count", 0) + 1
        state["current_agent"] = "download_agent"
        print(f"🔄 Retrying... (Attempt {state['retry_count']})")
    else:
        print("🛑 Max retries reached. Analysis failed.")
        state["current_agent"] = "failed"
    
    return state
