import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from tools.extract_skills import extract_skills_from_pdf
from agents.candidate_guidance_agent import CandidateGuidanceAgent

# ===================== APP SETUP =====================

app = FastAPI(title="KAMIRecruit AI Backend")

# Allow all CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------- Serve React build (Vite) --------
DIST_DIR = "frontend/dist"
ASSETS_DIR = os.path.join(DIST_DIR, "assets")

if os.path.exists(DIST_DIR):
    # Serve JS/CSS assets at /assets/*
    if os.path.exists(ASSETS_DIR):
        app.mount("/assets", StaticFiles(directory=ASSETS_DIR), name="assets")
    else:
        print("⚠️ WARNING: frontend/dist/assets not found — Vite assets missing")
else:
    print("⚠️ WARNING: frontend/dist not found — React build missing")


# ===================== MODELS =====================

class ChatRequest(BaseModel):
    message: str


# ===================== AI AGENT =====================

agent = CandidateGuidanceAgent()


# ===================== API ROUTES =====================

@app.post("/api/chat")
async def chat_api(data: ChatRequest):
    reply = agent.chat(data.message)
    return {"reply": reply}


@app.post("/api/process_resume")
async def process_resume(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")

    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(await file.read())

    try:
        skills = extract_skills_from_pdf(temp_path)
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

    return {"skills": skills}


@app.get("/api/health")
def health():
    return {"status": "ok", "message": "Backend running"}


# ===================== FRONTEND ROUTES =====================

@app.get("/", include_in_schema=False)
async def serve_root():
    """
    Serve the built React app (Vite) index.html at root.
    """
    index_path = os.path.join(DIST_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"error": "Frontend build not found. Run 'npm run build' in /frontend."}


@app.get("/{full_path:path}", include_in_schema=False)
async def serve_spa(full_path: str):
    """
    SPA fallback:
    - Any non-API route returns index.html
    - /api/* are reserved for backend
    """
    if full_path.startswith("api"):
        raise HTTPException(status_code=404, detail="Not Found")

    index_path = os.path.join(DIST_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)

    raise HTTPException(status_code=404, detail="Frontend build not found")
