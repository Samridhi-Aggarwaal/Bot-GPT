"""
Document schemas for RAG
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class DocumentCreate(BaseModel):
    """Schema for creating a new document"""
    title: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1)


class DocumentResponse(BaseModel):
    """Schema for document response"""
    id: int
    title: str
    created_at: datetime
    chunk_count: Optional[int] = 0
    
    class Config:
        from_attributes = True
