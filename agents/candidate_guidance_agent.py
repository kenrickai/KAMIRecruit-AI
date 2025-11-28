import os
from google import genai
from memory.memory import load_memory

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


class CandidateGuidanceAgent:

    def chat(self, user_id: int, message: str):
        memory = load_memory(user_id)
        history = memory.get("history", [])[-6:]

        prompt = f"""
You are the Talent-for-Good AI agent.

Your job is to:
1) Answer questions
2) Use tools when necessary
3) ALWAYS return JSON with:
   - "type": "text" or "action"
   - "payload": the text or the action args

Do NOT return plain text.
"""

        tools = [
            {
                "name": "search_projects",
                "description": "Search NGO projects based on a required skill",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "skill": {"type": "string"}
                    },
                    "required": ["skill"],
                }
            }
        ]

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt + "\nUser: " + message,
            tools=tools,
        )

        return response  # Return raw structure
