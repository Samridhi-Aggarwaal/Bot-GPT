from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services import rag_service, conversation_service
from typing import List

router = APIRouter()

@router.post("/upload")
async def upload_document(conversation_id: str, file: UploadFile = File(...)):
    conv = conversation_service.get_conversation(conversation_id)
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    content = await file.read()
    text = content.decode('utf-8', errors='ignore')
    doc = rag_service.add_document(conversation_id, file.filename, text)
    return {"document_id": doc["id"], "chunks": len(doc["chunks"])}
