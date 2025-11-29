# agents/candidate_guidance_agent.py

import os
import google.generativeai as genai
from memory.memory import load_memory

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


class CandidateGuidanceAgent:

    def chat(self, user_id: int, message: str) -> str:
        memory = load_memory(user_id)
        history = memory.get("history", [])[-6:]

        prompt = f"""
You are the Talent-for-Good AI agent.

User ID: {user_id}
Recent history: {history}

Your job is to:
1) Answer questions
2) Use tools when necessary
3) ALWAYS speak to the user in clear, friendly language.

User message:
{message}
"""

        # (you can keep your tools definition here if you want, no problem)

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )

        # ✅ Return plain text, not raw object
        return getattr(response, "text", "") or "[No response from Gemini]"
