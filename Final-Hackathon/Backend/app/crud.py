from .db import collection,feedback_logs_collection
from datetime import datetime
from bson import ObjectId

# Save a new evaluation into MongoDB with a timestamp
async def save_evaluation(result: dict):
    result["timestamp"] = datetime.utcnow()
    await collection.insert_one(result)

# Retrieve all evaluations, converting ObjectId to str for JSON serialization
async def get_evaluations():
    evaluations = []
    async for doc in collection.find():
        doc["_id"] = str(doc["_id"])  # Convert ObjectId to string
        evaluations.append(doc)
    return evaluations

async def save_feedback_log(log_data: dict):
    await feedback_logs_collection.insert_one(log_data)

# Get logs for a specific YouTube URL
async def get_feedback_logs(youtube_url: str):
    return await feedback_logs_collection.find_one({"youtube_url": youtube_url})

