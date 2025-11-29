"""
Message schemas
"""
from pydantic import BaseModel, Field
from datetime import datetime


class MessageCreate(BaseModel):
    """Schema for creating a new message"""
    content: str = Field(..., min_length=1, max_length=10000)


class MessageResponse(BaseModel):
    """Schema for message response"""
    id: int
    conversation_id: int
    role: str
    content: str
    tokens_used: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class MessagePairResponse(BaseModel):
    """Schema for user message + assistant response pair"""
    user_message: MessageResponse
    assistant_message: MessageResponse
