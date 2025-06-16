import google.generativeai as genai
import re
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Read API keys from environment
GEMINI_API_KEY1 = os.getenv("GEMINI_API_KEY1")

def analyze_section_with_gemini(section_title, section_text):
    genai.configure(api_key=GEMINI_API_KEY1)
    model = genai.GenerativeModel("gemini-2.0-flash")
    prompt = f"""
You are an expert in academic writing.

Analyze the following section titled '{section_title}' and classify it as either:
- Human-written
- AI-generated

Do not explain the reasoning. Just reply with one of the following: "Human-written" or "AI-generated".

Section:
{section_text[:3000]}
"""
    response = model.generate_content(prompt)
    return response.text.strip()
