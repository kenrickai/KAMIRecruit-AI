import os
import google.generativeai as genai

class CandidateGuidanceAgent:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def chat(self, message: str) -> str:
        try:
            result = self.model.generate_content(message)
            return result.text
        except Exception as e:
            return f"⚠️ Error: {str(e)}"
