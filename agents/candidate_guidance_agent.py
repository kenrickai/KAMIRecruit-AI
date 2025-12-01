import os
import requests

class CandidateGuidanceAgent:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")

        # v1beta REST text model endpoint
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

            r = requests.post(
                f"{self.url}?key={self.api_key}",
                json=payload,
                timeout=20
            )

            data = r.json()

            # 1️⃣ handle API errors
            if "error" in data:
                return f"⚠️ API Error: {data['error'].get('message')}"

            # 2️⃣ handle missing candidates
            if "candidates" not in data:
                return f"⚠️ API Error: Response missing candidates: {data}"

            # 3️⃣ extract text
            return data["candidates"][0]["content"]["parts"][0]["text"]

        except Exception as e:
            return f"⚠️ REST API Error: {str(e)}"
