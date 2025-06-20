from fastapi import APIRouter, HTTPException, FastAPI
from fastapi.encoders import jsonable_encoder
from app.models import VideoInput, EvaluationResult
from app.crud import save_evaluation, get_evaluations,save_feedback_log,get_feedback_logs
from core.runner import run_pitch_analysis
from bson import ObjectId
from fastapi.middleware.cors import CORSMiddleware

router = APIRouter()


@router.post("/analyze", response_model=EvaluationResult)
async def analyze_pitch(video: VideoInput):
    try:
        # Convert HttpUrl to plain string
        youtube_url = str(video.youtube_url)

        # Pass plain string to LangGraph system
        state = run_pitch_analysis(youtube_url)

        if state["current_agent"] != "completed":
            raise HTTPException(status_code=500, detail=state.get("error_message", "Unknown error"))

        report = state["final_report"]
        result = {
            "youtube_url": youtube_url,
            "overall_score": report["overall_score"],
            "scores": report["scores"],
            "report": report["detailed_report"],
            "metadata": state["metadata"]
        }

        await save_evaluation(result)
        await save_feedback_log({
    "youtube_url": youtube_url,
    "feedback": report["detailed_report"],
    "metadata": state["metadata"]
})

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"500: {str(e)}")


@router.get("/evaluations")
async def fetch_all_evaluations():
    return await get_evaluations()

@router.get("/feedback_logs")
async def fetch_feedback_logs(youtube_url: str):
    cleaned_url = youtube_url.strip()
    log = await get_feedback_logs(cleaned_url)

    if not log:
        raise HTTPException(status_code=404, detail="Log not found")

    return jsonable_encoder(log, custom_encoder={ObjectId: str})
