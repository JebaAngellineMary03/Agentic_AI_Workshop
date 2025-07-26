from dotenv import load_dotenv
import google.generativeai as genai
from langchain_core.messages import AIMessage
import os

load_dotenv()  # Loads from .env

api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("No API key found. Please set either GEMINI_API_KEY or GOOGLE_API_KEY environment variable.")

genai.configure(api_key=api_key)

def call_gemini(prompt: str) -> AIMessage:
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)
        return AIMessage(content=response.text)
    except Exception as e:
        return AIMessage(content=f"Error calling Gemini API: {str(e)}")
