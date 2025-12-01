import os
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv

from agents.candidate_guidance_agent import CandidateGuidanceAgent
from tools.extract_skills import extract_skills_from_pdf

load_dotenv()

app = FastAPI(title="KAMIRecruit AI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = CandidateGuidanceAgent()


class ChatRequest(BaseModel):
    message: str


@app.get("/")
async def root():
    return {"status": "running", "model": "gemini-pro-rest"}


# =============== CHAT ===============

@app.post("/api/chat")
async def chat_endpoint(req: ChatRequest):
    reply = agent.chat(req.message)
    return {"reply": reply}


# =============== PROCESS RESUME ===============

@app.post("/api/process_resume")
async def process_resume(file: UploadFile = File(...)):
    temp_path = f"temp_{file.filename}"

    with open(temp_path, "wb") as f:
        f.write(await file.read())

    try:
        skills = extract_skills_from_pdf(temp_path)
    finally:
        os.remove(temp_path)

    return {"skills": skills}


# Admin & static pages
@app.get("/admin")
async def admin_dashboard():
    return FileResponse("frontend/admin.html")
