import os
import requests

class CandidateGuidanceAgent:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")

        # REST endpoint for Gemini-Pro (text model)
        self.url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            "gemini-pro:generateContent"
        )

    def chat(self, message: str) -> str:
        try:
            payload = {
                "contents": [
                    {
                        "parts": [
                            {"text": message}
                        ]
                    }
                ]
            }

            response = requests.post(
                f"{self.url}?key={self.api_key}",
                json=payload,
                timeout=10
            )

            data = response.json()

            # Extract response safely
            return data["candidates"][0]["content"]["parts"][0]["text"]

        except Exception as e:
            return f"⚠️ REST API Error: {str(e)}"
