import os
import shutil
import time
import logging
from typing import List, Optional

from fastapi import FastAPI, HTTPException, UploadFile, File, Depends, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session

from memory.memory import append_history, load_memory
from router.agent_router import route_message, RouteDecision
from agents.orchestrator import Orchestrator
from tools.database_tool import (
    init_db,
    get_db_session,
    User,
    Project,
    Certificate,
    ChatMessage,
)
from tools.pdf_tool import extract_text_from_pdf
from tools.extract_skills import extract_skills

# -------------------------------------------------------
#                FASTAPI APP + LOGGING
# -------------------------------------------------------

app = FastAPI(title="Talent App - Multi-Agent System")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("talent_app")

orchestrator = Orchestrator()

# Basic in-memory metrics
METRICS = {
    "total_requests": 0,
    "total_chats": 0,
    "total_errors": 0,
}


# -------------------------------------------------------
#                   MIDDLEWARE (OBSERVABILITY)
# -------------------------------------------------------

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Logs execution time of each request for observability."""
    start = time.time()
    response = await call_next(request)
    duration = (time.time() - start) * 1000

    logger.info(
        f"{request.method} {request.url.path} "
        f"status={response.status_code} "
        f"took={duration:.2f}ms"
    )
    return response


# -------------------------------------------------------
#                   PYDANTIC MODELS
# -------------------------------------------------------

class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserRead(BaseModel):
    id: int
    username: str
    email: str
    skills: Optional[str] = None

    class Config:
        orm_mode = True


class ProjectCreate(BaseModel):
    title: str
    description: Optional[str] = None
    required_skills: Optional[str] = None


class ProjectRead(BaseModel):
    id: int
    title: str
    description: Optional[str]
    required_skills: Optional[str]

    class Config:
        orm_mode = True


class CertificateCreate(BaseModel):
    name: str
    issuer: Optional[str] = None


class CertificateRead(BaseModel):
    id: int
    name: str
    issuer: Optional[str]

    class Config:
        orm_mode = True


class ChatRequest(BaseModel):
    user_id: int
    message: str


class ChatResponse(BaseModel):
    reply: str
    route: RouteDecision
    history: list


class ResumeProcessResponse(BaseModel):
    message: str
    file_saved_as: str
    extracted_skills: List[str]


# -------------------------------------------------------
#                   STARTUP EVENT
# -------------------------------------------------------

@app.on_event("startup")
def on_startup():
    init_db()
    os.makedirs("uploads", exist_ok=True)
    logger.info("🚀 Talent App server started successfully.")


# -------------------------------------------------------
#                     USER ENDPOINTS
# -------------------------------------------------------

@app.post("/users", response_model=UserRead)
def create_user(payload: UserCreate, db: Session = Depends(get_db_session)):
    existing = db.query(User).filter(
        (User.username == payload.username) | (User.email == payload.email)
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Username or email already exists.")

    user = User(
        username=payload.username,
        email=payload.email,
        password=payload.password,  # NOTE: hash in production
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@app.get("/users/{user_id}", response_model=UserRead)
def get_user(user_id: int, db: Session = Depends(get_db_session)):
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return user


# -------------------------------------------------------
#                   PROJECT ENDPOINTS
# -------------------------------------------------------

@app.post("/users/{user_id}/projects", response_model=ProjectRead)
def create_project(user_id: int, payload: ProjectCreate, db: Session = Depends(get_db_session)):
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    project = Project(
        user_id=user_id,
        title=payload.title,
        description=payload.description,
        required_skills=payload.required_skills,
    )
    db.add(project)
    db.commit()
    db.refresh(project)

    return project


@app.get("/users/{user_id}/projects", response_model=List[ProjectRead])
def list_projects(user_id: int, db: Session = Depends(get_db_session)):
    return db.query(Project).filter(Project.user_id == user_id).all()


# -------------------------------------------------------
#                 CERTIFICATE ENDPOINTS
# -------------------------------------------------------

@app.post("/users/{user_id}/certificates", response_model=CertificateRead)
def create_certificate(user_id: int, payload: CertificateCreate, db: Session = Depends(get_db_session)):
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    cert = Certificate(
        user_id=user_id,
        name=payload.name,
        issuer=payload.issuer,
    )
    db.add(cert)
    db.commit()
    db.refresh(cert)

    return cert


@app.get("/users/{user_id}/certificates", response_model=List[CertificateRead])
def list_certificates(user_id: int, db: Session = Depends(get_db_session)):
    return db.query(Certificate).filter(Certificate.user_id == user_id).all()


# -------------------------------------------------------
#               MULTI-AGENT CHAT ENDPOINT
# -------------------------------------------------------

@app.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest, db: Session = Depends(get_db_session)):
    METRICS["total_requests"] += 1
    METRICS["total_chats"] += 1

    user = db.query(User).get(payload.user_id)
    if not user:
        METRICS["total_errors"] += 1
        raise HTTPException(status_code=404, detail="User not found.")

    # Save user message in DB
    db.add(ChatMessage(user_id=user.id, sender="user", message=payload.message))
    db.commit()

    # Multi-agent orchestration
    try:
        orch = orchestrator.handle(user.id, payload.message)
        reply_text = orch.reply
    except Exception as e:
        METRICS["total_errors"] += 1
        logger.exception("Error in orchestrator")
        reply_text = f"An error occurred: {e}"
        orch = RouteDecision(target="error", reason=str(e))

    # Update memory
    append_history(user.id, "user", payload.message)
    append_history(user.id, "ai", reply_text)
    history = load_memory(user.id).get("history", [])

    # Save AI reply to DB
    db.add(ChatMessage(user_id=user.id, sender="ai", message=reply_text))
    db.commit()

    return ChatResponse(reply=reply_text, route=orch, history=history)


# -------------------------------------------------------
#               RESUME PROCESS ENDPOINT
# -------------------------------------------------------

@app.post("/process_resume", response_model=ResumeProcessResponse)
async def process_resume(user_id: int, file: UploadFile = File(...), db: Session = Depends(get_db_session)):
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    uploads_dir = "uploads"
    os.makedirs(uploads_dir, exist_ok=True)

    file_path = os.path.join(uploads_dir, file.filename)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    text = extract_text_from_pdf(file_path)
    skills = extract_skills(text)

    user.skills = ",".join(skills)
    db.commit()

    return ResumeProcessResponse(
        message="Resume processed successfully",
        file_saved_as=file.filename,
        extracted_skills=skills,
    )


# -------------------------------------------------------
#                 OBSERVABILITY: METRICS
# -------------------------------------------------------

@app.get("/metrics")
def get_metrics():
    return METRICS


# -------------------------------------------------------
#            AGENT EVALUATION ENDPOINT
# -------------------------------------------------------

class EvalCase(BaseModel):
    message: str
    expected_contains: str


EVAL_CASES = [
    EvalCase(message="I want to find volunteer data projects.", expected_contains="project"),
    EvalCase(message="How can I improve my skills?", expected_contains="skill"),
]


@app.get("/evaluate")
def evaluate_agents(user_id: int = 1, db: Session = Depends(get_db_session)):
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    results = []
    passed = 0

    for case in EVAL_CASES:
        out = orchestrator.handle(user_id=user.id, message=case.message)
        ok = case.expected_contains in out.reply.lower()
        if ok:
            passed += 1

        results.append({
            "message": case.message,
            "expected_contains": case.expected_contains,
            "reply": out.reply,
            "agent": out.agent_name,
            "passed": ok
        })

    return {
        "total_cases": len(EVAL_CASES),
        "passed": passed,
        "score": passed / len(EVAL_CASES),
        "cases": results,
    }
