import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from tools.extract_skills import extract_skills_from_pdf
from agents.candidate_guidance_agent import CandidateGuidanceAgent

load_dotenv()

app = FastAPI(title="KAMIRecruit AI Backend")

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve frontend files
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

# Initialize AI agent
candidate_agent = CandidateGuidanceAgent()


# ========================== ROUTES ===============================

@app.get("/", response_class=HTMLResponse)
async def home():
    """Landing page."""
    return FileResponse("frontend/index.html")


@app.get("/admin", response_class=HTMLResponse)
async def admin():
    """Admin dashboard."""
    return FileResponse("frontend/admin.html")


# ====================== PROCESS RESUME ===========================

@app.post("/api/process_resume")
async def process_resume(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")

    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(await file.read())

    try:
        skills = extract_skills_from_pdf(temp_path)
    finally:
        os.remove(temp_path)

    return {"skills": skills}


# ====================== CHAT WITH AI ============================

@app.post("/api/chat")
async def chat_route(payload: dict):
    message = payload.get("message")
    if not message:
        raise HTTPException(status_code=400, detail="Message is required")

    reply = candidate_agent.chat(message)
    return {"reply": reply}


# ====================== HEALTH CHECK ============================

@app.get("/api/health")
async def health():
    return {"status": "ok", "message": "Backend running"}
