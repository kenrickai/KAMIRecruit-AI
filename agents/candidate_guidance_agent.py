import os
import google.generativeai as genai

class CandidateGuidanceAgent:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        genai.configure(api_key=api_key)

        # This is the correct model name for the NEW API
        self.model = "models/gemini-1.5-flash"

    def chat(self, message: str) -> str:
        try:
            response = genai.GenerativeModel(self.model).generate({"contents": message})
            return response.text
        except Exception as e:
            return f"⚠️ Error: {str(e)}"
