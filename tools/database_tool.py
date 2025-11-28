from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base

DATABASE_URL = "sqlite:///./talent.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    role = Column(String)
    skills = Column(Text)  # comma-separated string

    messages = relationship("ChatMessage", back_populates="user")


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    required_skills = Column(Text)


class Certificate(Base):
    __tablename__ = "certificates"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    project_id = Column(Integer)
    title = Column(String)


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    sender = Column(String)
    message = Column(Text)

    user = relationship("User", back_populates="messages")


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db_session():
    return SessionLocal()
