from langchain_core.tools import tool
from typing import Dict, Any
from utils.youtube_utils import download_audio_from_youtube, get_youtube_metadata
from chains.transcript_chain import extract_transcript
from chains.metadata_chain import extract_audio_features

@tool
def download_and_extract_tool(youtube_url: str) -> Dict[str, Any]:
    """Download audio and extract basic features from YouTube video"""
    try:
        print("📥 Downloading audio...")
        audio_path = download_audio_from_youtube(youtube_url)

        print("🧠 Extracting transcript...")
        transcript = extract_transcript(audio_path)

        print("🧾 Extracting metadata...")
        metadata = get_youtube_metadata(youtube_url)

        print("🎧 Extracting audio features...")
        audio_features = extract_audio_features(audio_path)

        return {
            "transcript": transcript,
            "metadata": metadata,
            "audio_features": audio_features,
            "audio_path": audio_path,
            "success": True
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
