"""
Conversation schemas
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class ConversationCreate(BaseModel):
    """Schema for creating a new conversation"""
    user_id: int
    first_message: str = Field(..., min_length=1, max_length=10000)
    mode: str = Field(default="open", pattern="^(open|rag)$")
    document_ids: Optional[List[int]] = []


class ConversationResponse(BaseModel):
    """Schema for conversation summary (list view)"""
    id: int
    user_id: int
    title: Optional[str]
    mode: str
    message_count: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class MessageInConversation(BaseModel):
    """Schema for message in conversation detail"""
    id: int
    role: str
    content: str
    tokens_used: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class ConversationDetailResponse(BaseModel):
    """Schema for conversation detail with full message history"""
    id: int
    user_id: int
    title: Optional[str]
    mode: str
    messages: List[MessageInConversation]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ConversationListResponse(BaseModel):
    """Schema for paginated conversation list"""
    conversations: List[ConversationResponse]
    total: int
    page: int
    limit: int
