from fastapi import APIRouter, HTTPException, FastAPI
from fastapi.encoders import jsonable_encoder
from app.models import VideoInput, EvaluationResult
from app.crud import save_evaluation, get_evaluations,save_feedback_log,get_feedback_logs
from core.runner import run_pitch_analysis
from bson import ObjectId
from fastapi.middleware.cors import CORSMiddleware
import logging

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

        # Extracting report data
        report = state["final_report"]
        result = {
            "youtube_url": youtube_url,
            "overall_score": report["overall_score"],
            "scores": report["scores"],
            "report": report["detailed_report"],
            "metadata": state["metadata"]
        }

        # Save evaluation result and feedback log
        await save_evaluation(result)
        await save_feedback_log({
            "youtube_url": youtube_url,
            "feedback": report["detailed_report"],
            "metadata": state["metadata"]
        })

        return result

    except ValueError as ve:
        # Handling specific errors (e.g., data issues)
        logging.error(f"Value error occurred: {str(ve)}")
        raise HTTPException(status_code=400, detail=f"Bad Request: {str(ve)}")

    except KeyError as ke:
        # Handling missing keys in data (e.g., missing field in the report or state)
        logging.error(f"Key error occurred: {str(ke)}")
        raise HTTPException(status_code=400, detail=f"Key Error: {str(ke)}")

    except HTTPException as http_err:
        # Catch HTTPException errors to handle specific HTTP issues
        logging.error(f"HTTP error occurred: {str(http_err.detail)}")
        raise http_err  # Re-raise the same HTTP exception

    except Exception as e:
        # Catch all other exceptions
        logging.error(f"Unexpected error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

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
