from pydantic import BaseModel, HttpUrl,Field
from typing import Dict, Any, Optional
from datetime import datetime

class VideoInput(BaseModel):
    youtube_url: HttpUrl

class EvaluationResult(BaseModel):
    youtube_url: str
    overall_score: int
    scores: Dict[str, int]
    report: str
    metadata: Dict[str, Any]

class FeedbackLog(BaseModel):
    youtube_url: str
    feedback: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Optional[Dict[str, Any]] = None
