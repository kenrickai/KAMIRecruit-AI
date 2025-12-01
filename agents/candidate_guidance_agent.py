import os
import google.generativeai as genai

class CandidateGuidanceAgent:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=api_key)

        # use the correct NEW model name
        self.model = "models/gemini-1.5-flash"

    def chat(self, message: str) -> str:
        try:
            response = genai.generate_text(
                model=self.model,
                prompt=message
            )
            return response.result
        except Exception as e:
            return f"⚠️ Error: {str(e)}"
