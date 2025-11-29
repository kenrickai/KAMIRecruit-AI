import os
from datetime import datetime
from typing import Generator

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    DateTime,
)
from sqlalchemy.orm import sessionmaker, relationship, declarative_base, Session

# --- DB URL configuration ---

DEFAULT_SQLITE_URL = "sqlite:///./talent.db"
DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_SQLITE_URL)

# Ensure /var/data exists when using a Render disk
if DATABASE_URL.startswith("sqlite:////var/data"):
    os.makedirs("/var/data", exist_ok=True)

# --- SQLAlchemy setup ---

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# --- Models ---

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    skills = Column(Text, nullable=True)

    projects = relationship("Project", back_populates="user", cascade="all, delete-orphan")
    certificates = relationship("Certificate", back_populates="user", cascade="all, delete-orphan")
    messages = relationship("ChatMessage", back_populates="user", cascade="all, delete-orphan")


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    required_skills = Column(Text, nullable=True)  # comma-separated

    user = relationship("User", back_populates="projects")


class Certificate(Base):
    __tablename__ = "certificates"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(255), nullable=False)
    issuer = Column(String(255), nullable=True)

    user = relationship("User", back_populates="certificates")


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    sender = Column(String(20), nullable=False)  # "user" | "ai"
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="messages")


# --- DB helpers ---

def init_db() -> None:
    """Create tables if they don't exist."""
    Base.metadata.create_all(bind=engine)
    print("[database_tool] Database initialized.")


def get_db_session() -> Generator[Session, None, None]:
    """
    FastAPI dependency: yields a Session and ensures it's closed.
    Usage: db: Session = Depends(get_db_session)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_db() -> Session:
    """
    Non-FastAPI usage (e.g. tools/search_tool.py).
    Returns a Session you must close manually.
    """
    return SessionLocal()
