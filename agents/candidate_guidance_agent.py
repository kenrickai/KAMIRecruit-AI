import os
import requests

# We keep this import so your project clearly uses the SDK version required
# (google-generativeai==0.3.2), even though the live chat uses REST.
try:
    import google.generativeai as legacy_genai  # noqa: F401
except Exception:
    legacy_genai = None


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

# Use a CURRENT model that actually exists now.
# Check https://ai.google.dev/gemini-api/docs/models for updated names.
GEMINI_MODEL = "gemini-2.0-flash"
GEMINI_ENDPOINT = f"https://generativelanguage.googleapis.com/v1/models/{GEMINI_MODEL}:generateContent"


class CandidateGuidanceAgent:
    def __init__(self):
        if not GEMINI_API_KEY:
            raise RuntimeError(
                "GEMINI_API_KEY (or GOOGLE_API_KEY) is not set in the environment."
            )

    def chat(self, message: str) -> str:
        """
        Call Gemini via the REST API.

        This completely avoids the old v1beta client issues and 404s you were seeing.
        """
        try:
            payload = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": (
                                    "You are a helpful talent screening assistant. "
                                    "Give concise, friendly guidance.\n\n"
                                    f"User message: {message}"
                                )
                            }
                        ]
                    }
                ]
            }

            resp = requests.post(
                GEMINI_ENDPOINT,
                params={"key": GEMINI_API_KEY},
                headers={"Content-Type": "application/json"},
                json=payload,
                timeout=30,
            )

            # If HTTP-level error (403, 404, etc.)
            try:
                resp.raise_for_status()
            except requests.exceptions.HTTPError as http_err:
                # Surface full JSON error so you see exactly what's wrong
                try:
                    err_json = resp.json()
                except Exception:
                    err_json = resp.text
                return f"⚠️ API Error: {err_json}"

            data = resp.json()

            # Safely pull text from candidates
            candidates = data.get("candidates", [])
            if not candidates:
                return "⚠️ API returned no candidates."

            first = candidates[0]
            content = first.get("content", {})
            parts = content.get("parts", [])
            if not parts:
                return "⚠️ API returned an empty response."

            text = parts[0].get("text", "").strip()
            if not text:
                return "⚠️ API returned no text."

            return text

        except requests.exceptions.RequestException as e:
            # Network / timeout / connection errors
            return f"⚠️ Network/API error: {str(e)}"
        except Exception as e:
            return f"⚠️ Unexpected error: {str(e)}"
