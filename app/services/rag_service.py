import uuid
from app.db.database import SessionLocal
from app.db import models
import math

CHUNK_SIZE = 500  # characters

def add_document(conversation_id: str, filename: str, content: str):
    db = SessionLocal()
    doc = models.Document(conversation_id=conversation_id, filename=filename, content=content)
    db.add(doc)
    db.commit()
    db.refresh(doc)
    # chunking
    chunks = []
    for i in range(0, len(content), CHUNK_SIZE):
        text = content[i:i+CHUNK_SIZE]
        chunk = models.Chunk(document_id=doc.id, text=text)
        db.add(chunk)
        chunks.append(chunk)
    db.commit()
    db.close()
    return {"id": doc.id, "chunks": len(chunks)}

def retrieve_top_k(conversation_id: str, query: str, k: int=3):
    # naive keyword match across chunks
    db = SessionLocal()
    conv = db.query(models.Conversation).filter(models.Conversation.id == conversation_id).first()
    if not conv:
        db.close()
        return []
    chunks = db.query(models.Chunk).join(models.Document, models.Chunk.document_id == models.Document.id).filter(models.Document.conversation_id==conversation_id).all()
    scored = []
    q = query.lower()
    for c in chunks:
        score = c.text.lower().count(q)
        if score>0:
            scored.append((score, c.text))
    scored.sort(reverse=True, key=lambda x: x[0])
    results = [t for s,t in scored][:k]
    db.close()
    return results
