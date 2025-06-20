from state.state import PitchAnalysisState
from tools import download_and_extract_tool

def start_analysis(state: PitchAnalysisState) -> PitchAnalysisState:
    """Initialize the analysis process"""
    print(f"🚀 Starting pitch analysis for: {state['youtube_url']}")
    state["current_agent"] = "download_agent"
    state["retry_count"] = 0
    return state

def download_agent(state: PitchAnalysisState) -> PitchAnalysisState:
    print("📥 Agent 1: Download and Extract")

    try:
        # ✅ FIX: Convert HttpUrl to string before passing to tool
        youtube_url_str = str(state["youtube_url"])
        print(f"📝 Processing URL: {youtube_url_str}")
        
        # Alternative approach - ensure it's definitely a string
        if hasattr(state["youtube_url"], 'unicode_string'):
            youtube_url_str = state["youtube_url"].unicode_string()
        elif hasattr(state["youtube_url"], '__str__'):
            youtube_url_str = str(state["youtube_url"])
        else:
            youtube_url_str = state["youtube_url"]
            
        result = download_and_extract_tool.invoke({
            "youtube_url": str(state["youtube_url"]),
            "verbose": True
        })

        if result["success"]:
            state["transcript"] = result["transcript"]
            state["metadata"] = result["metadata"]
            state["audio_features"] = result["audio_features"]
            state["audio_path"] = result["audio_path"]
            state["current_agent"] = "content_agent"
            print("✅ Download and extraction completed")
        else:
            state["error_message"] = result["error"]
            state["current_agent"] = "error"

    except Exception as e:
        print(f"❌ Error in download_agent: {str(e)}")
        state["error_message"] = str(e)
        state["current_agent"] = "error"

    return state