import os
import requests

class CandidateGuidanceAgent:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")

        # use REST (never breaks)
        self.api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

    def chat(self, message: str) -> str:
        try:
            payload = {
                "contents": [{"parts": [{"text": message}]}]
            }

            res = requests.post(
                f"{self.api_url}?key={self.api_key}",
                json=payload
            )

            data = res.json()

            if "candidates" in data:
                return data["candidates"][0]["content"]["parts"][0]["text"]

            return f"⚠️ API Error: {data}"

        except Exception as e:
            return f"⚠️ Exception: {str(e)}"
