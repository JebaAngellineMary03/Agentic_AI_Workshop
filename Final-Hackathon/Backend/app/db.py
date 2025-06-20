from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_URI)
db = client["pitch_analysis"]
collection = db["evaluations"]
feedback_logs_collection=db["feedback_logs"]
