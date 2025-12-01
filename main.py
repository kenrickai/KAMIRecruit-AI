import os

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from tools.extract_skills import extract_skills_from_pdf
from agents.candidate_guidance_agent import CandidateGuidanceAgent

# Load .env for local dev; on Render, env vars are set in the dashboard
load_dotenv()

app = FastAPI(title="KAMIRecruit AI Backend")

# CORS for your React frontend on Render
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],         # you can restrict this later
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve the built frontend (Vite dist) if you want from the backend
# (optional – you already have a separate frontend Render service)
if os.path.isdir("frontend/dist"):
    app.mount(
        "/",
        StaticFiles(directory="frontend/dist", html=True),
        name="frontend",
    )

# Initialize AI agent (REST-based Gemini)
try:
    candidate_agent = CandidateGuidanceAgent()
except Exception as e:
    # Don't crash the whole app – just log and keep endpoints alive
    print(">>> ERROR initializing CandidateGuidanceAgent:", str(e))
    candidate_agent = None


# ========================== ROUTES ===============================

@app.get("/legacy", response_class=HTMLResponse)
async def legacy_home():
    """
    Optional: legacy HTML landing if you still want to serve frontend/index.html
    from the backend root folder.
    """
    if not os.path.exists("frontend/index.html"):
        return HTMLResponse(
            "<h1>KAMIRecruit Backend</h1><p>No legacy index.html found.</p>",
            status_code=200,
        )
    return FileResponse("frontend/index.html")


@app.get("/admin", response_class=HTMLResponse)
async def admin():
    """Admin dashboard (legacy HTML)."""
    if not os.path.exists("frontend/admin.html"):
        return HTMLResponse(
            "<h1>Admin</h1><p>No admin.html found.</p>",
            status_code=200,
        )
    return FileResponse("frontend/admin.html")


# ====================== PROCESS RESUME ===========================

@app.post("/api/process_resume")
async def process_resume(file: UploadFile = File(...)):
    """
    Upload a resume PDF -> extract skills.
    """
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")

    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(await file.read())

    try:
        skills = extract_skills_from_pdf(temp_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {e}")
    finally:
        try:
            os.remove(temp_path)
        except FileNotFoundError:
            pass

    return {"skills": skills}


# ====================== CHAT WITH AI ============================

@app.post("/api/chat")
async def chat_route(payload: dict):
    """
    Chat endpoint used by your React frontend.
    """
    message = payload.get("message")
    if not message:
        raise HTTPException(status_code=400, detail="Message is required")

    if candidate_agent is None:
        raise HTTPException(
            status_code=500,
            detail="Candidate agent not initialized. Check GEMINI_API_KEY env var.",
        )

    reply = candidate_agent.chat(message)
    return {"reply": reply}


# ====================== HEALTH CHECK ============================

@app.get("/api/health")
async def health():
    return {
        "status": "ok",
        "message": "Backend running",
        "gemini_model": "gemini-2.0-flash",
    }
