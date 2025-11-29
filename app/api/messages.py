"""
Message API endpoints
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.message import MessageCreate, MessagePairResponse, MessageResponse
from app.services.conversation_service import ConversationService

router = APIRouter(prefix="/api/v1/conversations", tags=["messages"])
conversation_service = ConversationService()


@router.post("/{conversation_id}/messages", response_model=MessagePairResponse, status_code=201)
def add_message(
    conversation_id: int,
    message_data: MessageCreate,
    db: Session = Depends(get_db)
):
    """
    Add a new message to a conversation and get LLM response
    
    - **conversation_id**: Conversation ID
    - **content**: Message content
    """
    user_message, assistant_message = conversation_service.add_message(
        db, conversation_id, message_data.content
    )
    
    return MessagePairResponse(
        user_message=MessageResponse(
            id=user_message.id,
            conversation_id=user_message.conversation_id,
            role=user_message.role,
            content=user_message.content,
            tokens_used=user_message.tokens_used,
            created_at=user_message.created_at
        ),
        assistant_message=MessageResponse(
            id=assistant_message.id,
            conversation_id=assistant_message.conversation_id,
            role=assistant_message.role,
            content=assistant_message.content,
            tokens_used=assistant_message.tokens_used,
            created_at=assistant_message.created_at
        )
    )
