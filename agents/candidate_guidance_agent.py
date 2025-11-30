# agents/candidate_guidance_agent.py

import os
import google.generativeai as genai
from memory.memory import load_memory

# Configure Gemini client with API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


class CandidateGuidanceAgent:
    """
    Provides personalized career & skill guidance using Gemini 2.0 Flash.
    Memory from local storage is used to generate context-aware responses.
    """

    def chat(self, user_id: int, message: str) -> str:
        # Load user memory
        memory = load_memory(user_id)
        history = memory.get("history", [])[-6:]

        prompt = f"""
You are a Career Guidance Agent helping job seekers improve their career, resume, and skills.

User ID: {user_id}

Recent interaction history:
{history}

User message:
{message}

Instructions:
- Be helpful, practical, and friendly.
- Use context from memory when relevant.
- Provide actionable next steps.
- Keep answers concise.
"""

        try:
            model = genai.GenerativeModel("gemini-2.0-flash")
            response = model.generate_content(prompt)
            return (response.text or "").strip()

        except Exception as e:
            return f"Error generating response: {e}"
