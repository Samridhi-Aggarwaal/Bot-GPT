from app.db.database import SessionLocal
from app.db import models
from datetime import datetime
from sqlalchemy.orm import joinedload

def create_conversation(user_id: str, first_message: str, mode: str = "open"):
    db = SessionLocal()
    conv = models.Conversation(user_id=user_id, mode=mode, title=(first_message[:50]))
    db.add(conv)
    db.commit()
    db.refresh(conv)
    # add first message
    msg = models.Message(conversation_id=conv.id, role="user", content=first_message)
    db.add(msg)
    conv.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(conv)
    db.close()
    return conv

def get_conversation(conv_id: str):
    db = SessionLocal()
    conv = db.query(models.Conversation).filter(models.Conversation.id == conv_id).first()
    db.close()
    return conv

def get_conversation_detail(conv_id: str):
    db = SessionLocal()
    conv = db.query(models.Conversation).options(joinedload(models.Conversation.messages)).filter(models.Conversation.id == conv_id).first()
    db.close()
    return conv

def list_conversations(user_id: str = None, page: int =1, page_size: int=20):
    db = SessionLocal()
    q = db.query(models.Conversation)
    if user_id:
        q = q.filter(models.Conversation.user_id == user_id)
    q = q.order_by(models.Conversation.updated_at.desc()).offset((page-1)*page_size).limit(page_size)
    res = q.all()
    db.close()
    return res

def add_message(conversation_id: str, role: str, content: str):
    db = SessionLocal()
    msg = models.Message(conversation_id=conversation_id, role=role, content=content)
    db.add(msg)
    conv = db.query(models.Conversation).filter(models.Conversation.id == conversation_id).first()
    conv.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(msg)
    db.close()
    return msg

def delete_conversation(conv_id: str):
    db = SessionLocal()
    conv = db.query(models.Conversation).filter(models.Conversation.id == conv_id).first()
    if conv:
        db.delete(conv)
        db.commit()
    db.close()

def build_context(conversation_id: str, max_messages: int = 8):
    db = SessionLocal()
    conv = db.query(models.Conversation).options(joinedload(models.Conversation.messages)).filter(models.Conversation.id == conversation_id).first()
    if not conv:
        db.close()
        return {"messages": [], "summary": ""}
    msgs = sorted(conv.messages, key=lambda m: m.timestamp)[-max_messages:]
    context = "\n".join([f"{m.role}: {m.content}" for m in msgs])
    summary = conv.summary or ""
    db.close()
    return {"messages": context, "summary": summary}
