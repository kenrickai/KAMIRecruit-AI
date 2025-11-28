# agents/task_recommender_agent.py

import os
from google import genai

from memory.memory import load_memory

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


class TaskRecommenderAgent:
    """
    Gives concrete next steps / mini-roadmaps for the user
    based on their message + stored memory.
    """

    def suggest(self, user_id: int, message: str) -> str:
        memory = load_memory(user_id)
        facts = memory.get("facts", [])
        skills = memory.get("skills", [])
        prefs = memory.get("preferences", [])

        prompt = f"""
You are a Task Recommender agent for Talent for Good.

User ID: {user_id}

Known facts: {facts}
Known skills: {skills}
Known preferences: {prefs}

User message:
{message}

Your job:
- Suggest 3–5 concrete, realistic next actions the user can take in the next 1–4 weeks.
- Focus on NGO projects, skill-building, and portfolio outcomes.
- Be encouraging but concise.
- Use short bullet points.

Respond directly with the final answer. No system messages, no meta commentary.
"""

        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt,
            )
            return response.text or "[No response from Gemini]"
        except Exception as e:
            return f"[TaskRecommender Gemini error: {str(e)}]"
