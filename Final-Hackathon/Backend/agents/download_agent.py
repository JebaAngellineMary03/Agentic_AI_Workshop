from langchain.agents import Tool, initialize_agent
from langchain.agents.agent_types import AgentType
from langchain_core.tools import tool
from typing import Dict, Any
from utils.youtube_utils import download_audio_from_youtube, get_youtube_metadata
from chains.transcript_chain import extract_transcript
from chains.metadata_chain import extract_audio_features
from state.state import PitchAnalysisState
from tools.download_and_extract import download_and_extract_tool
from llms.llms import llm

def start_analysis(state: PitchAnalysisState) -> PitchAnalysisState:
    """Initialize the analysis process"""
    print(f"🚀 Starting pitch analysis for: {state['youtube_url']}")
    state["current_agent"] = "download_agent"
    state["retry_count"] = 0
    return state

def download_agent(state: PitchAnalysisState) -> PitchAnalysisState:
    """Download and extract data from YouTube URL using LangChain agent"""
    print("📥 Agent 1: Download and Extract")

    try:
        # Ensure youtube_url is a string
        youtube_url_str = str(state["youtube_url"])
        print(f"📝 Processing URL: {youtube_url_str}")

        # Create a function that the LangChain agent can call
        def process_youtube_url(url: str) -> Dict[str, Any]:
            """Process YouTube URL and return results"""
            try:
                result = download_and_extract_tool.invoke({
                    "youtube_url": url,
                })
                return result
            except Exception as e:
                return {"success": False, "error": str(e)}

        # Tool definition for LangChain agent
        download_tool = Tool(
            name="ProcessYouTubeURL",
            func=process_youtube_url,
            description="Download audio and extract features from a YouTube video URL. Input should be a YouTube URL string."
        )

        # Initialize the LangChain agent executor
        agent_executor = initialize_agent(
            tools=[download_tool],
            llm=llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            max_iterations=3,
            early_stopping_method="generate"
        )

        # Run the agent with the YouTube URL
        agent_input = f"Process this YouTube URL and extract audio features: {youtube_url_str}"
        agent_result = agent_executor.run(agent_input)

        # The agent should have used the tool, so we need to get the actual result
        # Let's directly call our tool to get the structured result
        result = process_youtube_url(youtube_url_str)

        if result["success"]:
            # Update the state with results
            state["transcript"] = result["transcript"]
            state["metadata"] = result["metadata"]
            state["audio_features"] = result["audio_features"]
            state["audio_path"] = result["audio_path"]
            state["current_agent"] = "content_agent"
            print("✅ Download and extraction completed")
        else:
            state["error_message"] = result["error"]
            state["current_agent"] = "error_handler"
            print(f"❌ Error: {result['error']}")

    except Exception as e:
        state["error_message"] = str(e)
        state["current_agent"] = "error_handler"
        print(f"❌ Error in download_agent: {str(e)}")

    return state