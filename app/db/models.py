import uuid
from sqlalchemy import Column, String, Text, Integer, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

def gen_id(prefix="id"):
    return f"{prefix}_{uuid.uuid4().hex[:12]}"

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=lambda: gen_id("user"))
    email = Column(String, unique=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(String, primary_key=True, default=lambda: gen_id("conv"))
    user_id = Column(String, ForeignKey("users.id"), nullable=True)
    mode = Column(String, default="open")
    title = Column(String, nullable=True)
    summary = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="conversation", cascade="all, delete-orphan")

class Message(Base):
    __tablename__ = "messages"
    id = Column(String, primary_key=True, default=lambda: gen_id("msg"))
    conversation_id = Column(String, ForeignKey("conversations.id"))
    role = Column(String)
    content = Column(Text)
    token_count = Column(Integer, default=0)
    timestamp = Column(DateTime, default=datetime.utcnow)

    conversation = relationship("Conversation", back_populates="messages")

class Document(Base):
    __tablename__ = "documents"
    id = Column(String, primary_key=True, default=lambda: gen_id("doc"))
    conversation_id = Column(String, ForeignKey("conversations.id"))
    filename = Column(String)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    conversation = relationship("Conversation", back_populates="documents")

class Chunk(Base):
    __tablename__ = "chunks"
    id = Column(String, primary_key=True, default=lambda: gen_id("chunk"))
    document_id = Column(String, ForeignKey("documents.id"))
    text = Column(Text)
    # embedding would be stored in prod
    created_at = Column(DateTime, default=datetime.utcnow)
