import google.generativeai as genai

class CriticAgent:
    def __init__(self):
        genai.configure(api_key="AIzaSyCvpeCpwNe1auSU0jh_w6JssnlWnHrMc0Y")  # <-- Replace with your Gemini API key

    def review(self, content: str) -> str:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(f"Review this EDA report and suggest improvements:\n{content}")
        return response.text 