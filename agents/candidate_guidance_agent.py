import os
import google.generativeai as genai

class CandidateGuidanceAgent:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=api_key)

        # Correct model format for google-generativeai 0.7.2
        self.model = genai.GenerativeModel("models/gemini-1.5-flash")

        # Debug log (Render will print this)
        print(">>> USING MODEL:", "models/gemini-1.5-flash")

    def chat(self, message: str) -> str:
        try:
            response = self.model.generate_content(message)
            return response.text
        except Exception as e:
            return f"⚠️ Error: {str(e)}"
