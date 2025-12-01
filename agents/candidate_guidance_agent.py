import os
import requests

API_KEY = os.getenv("GEMINI_API_KEY")

# REST endpoint for Cloud Console API keys
MODEL = "models/gemini-pro"
ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/{MODEL}:generateContent?key={API_KEY}"

class CandidateGuidanceAgent:
    def chat(self, message: str):
        try:
            payload = {
                "contents": [
                    {
                        "parts": [{"text": message}]
                    }
                ]
            }

            response = requests.post(ENDPOINT, json=payload)
            data = response.json()

            if "candidates" not in data:
                return f"⚠️ API Error: {data}"

            return data["candidates"][0]["content"]["parts"][0]["text"]

        except Exception as e:
            return f"⚠️ Request Failed: {str(e)}"
