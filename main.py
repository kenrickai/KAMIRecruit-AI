import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from tools.extract_skills import extract_skills_from_pdf
from agents.candidate_guidance_agent import CandidateGuidanceAgent

# FastAPI app
app = FastAPI()

# Allow all CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Serve FRONTEND build folder ===
if os.path.exists("frontend/dist"):
    app.mount("/", StaticFiles(directory="frontend/dist", html=True), name="frontend")
else:
    print("⚠️ WARNING: frontend/dist not found — React build missing")

# === AI Agent ===
agent = CandidateGuidanceAgent()

class ChatRequest(BaseModel):
    message: str


# ======================== API ROUTES ========================

@app.post("/api/chat")
async def chat_api(data: ChatRequest):
    reply = agent.chat(data.message)
    return {"reply": reply}


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


@app.get("/api/health")
def health():
    return {"status": "ok"}
