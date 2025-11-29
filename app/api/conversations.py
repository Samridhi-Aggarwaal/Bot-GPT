"""
Conversation API endpoints
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.conversation import (
    ConversationCreate,
    ConversationResponse,
    ConversationListResponse,
    ConversationDetailResponse
)
from app.services.conversation_service import ConversationService

router = APIRouter(prefix="/api/v1/conversations", tags=["conversations"])
conversation_service = ConversationService()


@router.post("", response_model=ConversationDetailResponse, status_code=201)
def create_conversation(
    conversation_data: ConversationCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new conversation with the first message
    
    - **user_id**: User ID
    - **first_message**: First message content
    - **mode**: Conversation mode ('open' or 'rag')
    - **document_ids**: List of document IDs for RAG mode (optional)
    """
    conversation = conversation_service.create_conversation(db, conversation_data)
    
    return ConversationDetailResponse(
        id=conversation.id,
        user_id=conversation.user_id,
        title=conversation.title,
        mode=conversation.mode,
        messages=[
            {
                "id": msg.id,
                "role": msg.role,
                "content": msg.content,
                "tokens_used": msg.tokens_used,
                "created_at": msg.created_at
            }
            for msg in conversation.messages
        ],
        created_at=conversation.created_at,
        updated_at=conversation.updated_at
    )


@router.get("", response_model=ConversationListResponse)
def list_conversations(
    user_id: int = Query(..., description="User ID"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    """
    List all conversations for a user with pagination
    
    - **user_id**: User ID
    - **page**: Page number (default: 1)
    - **limit**: Items per page (default: 20, max: 100)
    """
    skip = (page - 1) * limit
    conversations, total = conversation_service.list_conversations(
        db, user_id, skip, limit
    )
    
    return ConversationListResponse(
        conversations=[
            ConversationResponse(
                id=conv.id,
                user_id=conv.user_id,
                title=conv.title,
                mode=conv.mode,
                message_count=len(conv.messages),
                created_at=conv.created_at,
                updated_at=conv.updated_at
            )
            for conv in conversations
        ],
        total=total,
        page=page,
        limit=limit
    )


@router.get("/{conversation_id}", response_model=ConversationDetailResponse)
def get_conversation(
    conversation_id: int,
    db: Session = Depends(get_db)
):
    """
    Get conversation details with full message history
    
    - **conversation_id**: Conversation ID
    """
    conversation = conversation_service.get_conversation(db, conversation_id)
    
    return ConversationDetailResponse(
        id=conversation.id,
        user_id=conversation.user_id,
        title=conversation.title,
        mode=conversation.mode,
        messages=[
            {
                "id": msg.id,
                "role": msg.role,
                "content": msg.content,
                "tokens_used": msg.tokens_used,
                "created_at": msg.created_at
            }
            for msg in conversation.messages
        ],
        created_at=conversation.created_at,
        updated_at=conversation.updated_at
    )


@router.delete("/{conversation_id}", status_code=204)
def delete_conversation(
    conversation_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a conversation and all its messages
    
    - **conversation_id**: Conversation ID
    """
    conversation_service.delete_conversation(db, conversation_id)
    return None
