import os
from google import genai  # NEW SDK

class CandidateGuidanceAgent:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-1.5-flash"

    def chat(self, message: str) -> str:
        try:
            response = self.client.responses.generate(
                model=self.model,
                contents=[message]
            )
            return response.text
        except Exception as e:
            return f"⚠️ Error: {str(e)}"
