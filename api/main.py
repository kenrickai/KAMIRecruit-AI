# main.py — multi-agent version with API key auth + routing

import sys
import os
import shutil

print("PYTHONPATH:", sys.path)

from fastapi import (
    FastAPI,
    HTTPException,
    UploadFile,
    File,
    Depends,
    Header,
)
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# JSON memory manager
from memory.memory import append_history

# Routing
from router.agent_router import route_message, RouteDecision

# SQLAlchemy models & DB helpers
from tools.database_tool import (
    init_db,
    get_db_session,
    User,
    Project,
    Certificate,
    ChatMessage,
)

# Resume parsing helpers
from tools.resume_parser import extract_text_from_pdf, extract_skills

# Agents
from agents.candidate_guidance_agent import CandidateGuidanceAgent
from agents.ngo_onboarding_agent import NGOOnboardingAgent
from agents.task_recommender_agent import TaskRecommenderAgent


# =========================================================
# FASTAPI APP + CORS
# =========================================================

app = FastAPI(title="Talent for Good - Multi-Agent Prototype with Auth")

# Allow calling from a static HTML file / localhost in dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # in production, tighten this!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize DB schema
init_db()

# Real agents
candidate_agent = CandidateGuidanceAgent()
ngo_agent = NGOOnboardingAgent()   # still simple stub, OK
task_agent = TaskRecommenderAgent()

# Directory for resume uploads
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# =========================================================
# API KEY AUTH (simple header-based)
# =========================================================

API_KEY = os.getenv("TFG_API_KEY")  # set this in your .env


def verify_api_key(x_api_key: str = Header(default=None)):
    """
    Simple API key check using X-API-Key header.

    - Set TFG_API_KEY in your .env (e.g. TFG_API_KEY=supersecret123)
    - Client must send:  X-API-Key: supersecret123
    """
    if not API_KEY:
        # Dev safeguard: force you to set the key
        raise HTTPException(
            status_code=500,
            detail="Server API key (TFG_API_KEY) is not configured.",
        )

    if x_api_key is None or x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key.",
        )


# =========================================================
# BASIC HEALTH CHECK
# =========================================================

@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "Talent for Good API running.",
    }


# =========================================================
# USER SIGNUP
# =========================================================

class SignupIn(BaseModel):
    name: str
    role: str
    skills: list[str] = []


@app.post("/signup")
def signup(payload: SignupIn):
    session = get_db_session()
    user = User(
        name=payload.name,
        role=payload.role,
        skills=",".join(payload.skills),
    )
    session.add(user)
    session.commit()
    return {"user_id": user.id, "name": user.name, "role": user.role}


# =========================================================
# PROJECT LISTING
# =========================================================

@app.get("/projects")
def list_projects():
    session = get_db_session()
    projects = session.query(Project).all()

    result: list[dict] = []
    for p in projects:
        skills = p.required_skills.split(",") if p.required_skills else []
        result.append(
            {
                "id": p.id,
                "title": p.title,
                "required_skills": skills,
            }
        )

    return result


@app.post("/projects/{project_id}/join", dependencies=[Depends(verify_api_key)])
def join_project(project_id: int, user_id: int):
    session = get_db_session()

    proj = session.get(Project, project_id)
    user = session.get(User, user_id)

    if proj is None or user is None:
        raise HTTPException(status_code=404, detail="not found")

    return {"status": "joined", "project": proj.title, "user": user.name}


# =========================================================
# AGENT START ENDPOINTS (simple)
# =========================================================

@app.post("/agents/candidate/{user_id}/start", dependencies=[Depends(verify_api_key)])
def start_candidate(user_id: int):
    return {"message": f"Candidate agent started for user {user_id}"}


@app.post("/agents/ngo/{ngo_id}/start", dependencies=[Depends(verify_api_key)])
def start_ngo(ngo_id: int):
    return {"message": f"NGO agent started for ngo {ngo_id}"}


# =========================================================
# BASIC CHAT (candidate-only, protected by API key)
# =========================================================

class ChatIn(BaseModel):
    message: str


@app.post("/chat/{user_id}", dependencies=[Depends(verify_api_key)])
def chat_with_ai(user_id: int, payload: ChatIn):
    """
    Original simple chat endpoint:
    - Always uses CandidateGuidanceAgent
    - Logs to DB + JSON memory
    """
    session = get_db_session()

    # 1) Save user message to DB
    user_msg = ChatMessage(
        user_id=user_id,
        sender="user",
        message=payload.message,
    )
    session.add(user_msg)
    session.commit()

    # 1b) Save user message to JSON memory
    append_history(user_id, "user", payload.message)

    # 2) Call Gemini candidate agent
    ai_text = candidate_agent.chat(user_id=user_id, message=payload.message)

    # 3) Save AI reply to DB
    ai_msg = ChatMessage(
        user_id=user_id,
        sender="ai",
        message=ai_text,
    )
    session.add(ai_msg)
    session.commit()

    # 3b) Save AI reply to JSON memory
    append_history(user_id, "ai", ai_text)

    return {"reply": ai_text}


# =========================================================
# SMART CHAT (with routing to multiple skills) — main one for frontend
# =========================================================

class SmartChatOut(BaseModel):
    reply: str
    route_target: str
    route_reason: str


@app.post(
    "/smart-chat/{user_id}",
    response_model=SmartChatOut,
    dependencies=[Depends(verify_api_key)],
)
def smart_chat(user_id: int, payload: ChatIn):
    """
    Advanced chat endpoint:
    - Uses router.agent_router.route_message to pick the right 'skill'
    - Candidate guidance / NGO / Resume / Search / Task planner
    - Logs to DB + JSON memory
    """
    session = get_db_session()

    # 0) Routing decision
    decision: RouteDecision = route_message(payload.message)

    # 1) Log USER message
    user_msg = ChatMessage(
        user_id=user_id,
        sender="user",
        message=payload.message,
    )
    session.add(user_msg)
    session.commit()

    append_history(user_id, "user", payload.message)

    # 2) Dispatch based on route target
    if decision.target == "candidate":
        ai_text = candidate_agent.chat(user_id=user_id, message=payload.message)

    elif decision.target == "ngo":
        # For now, reuse simple NGO agent stub
        ai_text = ngo_agent.start(ngo_id=user_id)

    elif decision.target == "resume":
        ai_text = (
            "It sounds like you're asking about resumes.\n\n"
            "Right now, I can *parse* resumes if you upload a PDF via "
            "`POST /upload-resume/{user_id}` in the docs UI. "
            "After uploading, I’ll update your skills in the system."
        )

    elif decision.target == "search":
        # Simple placeholder for future web/search integration
        ai_text = (
            "You’re asking for search/lookup.\n\n"
            "In this prototype I don’t hit the web yet, but you can:\n"
            "- Browse local NGO portals (e.g., UN Volunteers, Idealist)\n"
            "- Filter for data / research / monitoring roles\n"
            "Later we can plug this into a real search tool."
        )

    elif decision.target == "task":
        # Use TaskRecommenderAgent + Gemini to suggest concrete steps
        ai_text = task_agent.suggest(user_id=user_id, message=payload.message)

    else:
        # Fallback to candidate agent
        ai_text = candidate_agent.chat(user_id=user_id, message=payload.message)

    # 3) Log AI message
    ai_msg = ChatMessage(
        user_id=user_id,
        sender="ai",
        message=ai_text,
    )
    session.add(ai_msg)
    session.commit()

    append_history(user_id, "ai", ai_text)

    return SmartChatOut(
        reply=ai_text,
        route_target=decision.target,
        route_reason=decision.reason,
    )


# =========================================================
# RESUME UPLOAD + SKILL PARSER
# =========================================================

@app.post("/upload-resume/{user_id}", dependencies=[Depends(verify_api_key)])
def upload_resume(user_id: int, file: UploadFile = File(...)):
    session = get_db_session()

    user = session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # Save file to disk
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract text & detect skills
    text = extract_text_from_pdf(file_path)
    skills = extract_skills(text)

    # Save skills back to DB
    user.skills = ",".join(skills)
    session.commit()

    return {
        "message": "Resume processed successfully",
        "file_saved_as": file.filename,
        "extracted_skills": skills,
    }
