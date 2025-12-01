import os
import requests

class CandidateGuidanceAgent:
    def __init__(self):
        # Load your API key from environment variables
        self.api_key = os.getenv("GEMINI_API_KEY")

        # --- THIS is the REST endpoint. Leave it exactly like this. ---
        self.url = (
            "https://generativelanguage.googleapis.com/v1/models/"
            "gemini-pro:generateContent?key=" + self.api_key
        )
        # --------------------------------------------------------------

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
