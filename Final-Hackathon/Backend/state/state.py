from typing import TypedDict, Dict, Any

class PitchAnalysisState(TypedDict):
    youtube_url: str
    transcript: str
    metadata: Dict[str, Any]
    audio_features: Dict[str, Any]
    audio_path: str
    content_analysis: str
    clarity_tone_analysis: str
    structure_analysis: Dict[str, Any]
    final_report: Dict[str, Any]
    current_agent: str
    error_message: str
    retry_count: int
