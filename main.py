import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv

# Agents
from agents.candidate_guidance_agent import CandidateGuidanceAgent

# Tools
from tools.extract_skills import extract_skills_from_pdf

load_dotenv()

app = FastAPI(title="KAMIRECRUIT AI BACKEND")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# INIT AI AGENT
agent = CandidateGuidanceAgent()


# ------------------- HEALTH CHECK -------------------
@app.get("/api/health")
def health():
    return {"status": "ok", "message": "backend running"}


# ------------------- CHAT ENDPOINT -------------------
class ChatRequest(BaseModel):
    message: str

@app.post("/api/chat")
async def chat(req: ChatRequest):
    try:
        reply = agent.chat(req.message)
        return {"reply": reply}
    except Exception as e:
        return {"reply": f"⚠️ Backend Error: {str(e)}"}


# ------------------- RESUME PARSER -------------------
@app.post("/api/process_resume")
async def process_resume(file: UploadFile = File(...)):

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="PDF only")

    filepath = f"temp_{file.filename}"

    with open(filepath, "wb") as f:
        f.write(await file.read())

    skills = extract_skills_from_pdf(filepath)
    os.remove(filepath)

    return {"skills": skills}


# ------------------- FRONTEND SERVE -------------------
@app.get("/")
def root():
    return FileResponse("frontend/index.html")
