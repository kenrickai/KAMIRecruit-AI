import os
import requests

class CandidateGuidanceAgent:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")

        # AI Studio model ID
        self.model = "models/gemini-1.5-flash"

        # AI Studio REST endpoint
        self.url = f"https://generativelanguage.googleapis.com/v1beta/{self.model}:generateContent?key={self.api_key}"

    def chat(self, message: str):
        try:
            payload = {
                "contents": [
                    {
                        "parts": [{"text": message}]
                    }
                ]
            }

            response = requests.post(self.url, json=payload)
            data = response.json()

            if "candidates" not in data:
                return f"⚠️ API Error: {data}"

            return data["candidates"][0]["content"]["parts"][0]["text"]

        except Exception as e:
            return f"⚠️ Request Failed: {str(e)}"
