from fastapi import APIRouter, HTTPException, Depends, Path
from fastapi import status
from pydantic import BaseModel
from typing import List
from app.db import models, schemas
from app.services import conversation_service, llm_service

router = APIRouter()

class CreateConversationPayload(BaseModel):
    user_id: str
    first_message: str
    mode: str = "open"

@router.post("", status_code=status.HTTP_201_CREATED)
def create_conversation(payload: CreateConversationPayload):
    conv = conversation_service.create_conversation(payload.user_id, payload.first_message, payload.mode)
    return {"conversation_id": conv.id}

@router.post("/{conversation_id}/messages", status_code=status.HTTP_200_OK)
def add_message(conversation_id: str, body: schemas.MessageCreate):
    conv = conversation_service.get_conversation(conversation_id)
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    # persist user message
    user_msg = conversation_service.add_message(conversation_id, "user", body.content)
    # Build context and call LLM
    context = conversation_service.build_context(conversation_id)
    assistant_text, meta = llm_service.generate_response(context, body.content, conversation_id)
    assistant_msg = conversation_service.add_message(conversation_id, "assistant", assistant_text)
    return {"assistant_message": assistant_msg.content, "metrics": meta}

@router.get("", response_model=List[schemas.ConversationOut])
def list_conversations(user_id: str = None, page: int = 1, page_size: int = 20):
    return conversation_service.list_conversations(user_id, page, page_size)

@router.get("/{conversation_id}", response_model=schemas.ConversationDetail)
def get_conversation(conversation_id: str):
    conv = conversation_service.get_conversation_detail(conversation_id)
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conv

@router.delete("/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_conversation(conversation_id: str):
    conversation_service.delete_conversation(conversation_id)
    return {}
