import os
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class CandidateGuidanceAgent:
    def __init__(self):
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def chat(self, message: str) -> str:
        try:
            result = self.model.generate_content(message)
            return result.text
        except Exception as e:
            return f"⚠️ Error: {str(e)}"
