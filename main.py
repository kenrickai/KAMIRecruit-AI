import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agents.candidate_guidance_agent import CandidateGuidanceAgent

# ---------------------------------------------------
# FastAPI initialization
# ---------------------------------------------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------
# Load agent
# ---------------------------------------------------
agent = CandidateGuidanceAgent()


# ---------------------------------------------------
# Request Schema
# ---------------------------------------------------
class ChatRequest(BaseModel):
    message: str


# ---------------------------------------------------
# Chat API
# ---------------------------------------------------
@app.post("/api/chat")
async def chat_api(req: ChatRequest):
    reply = agent.chat(req.message)
    return {"reply": reply}


# ---------------------------------------------------
# Health Check
# ---------------------------------------------------
@app.get("/")
def home():
    return {
        "status": "Backend is running",
        "model": "REST: gemini-pro:generateContent"
    }
