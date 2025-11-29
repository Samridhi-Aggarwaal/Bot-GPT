from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class MessageCreate(BaseModel):
    content: str

class MessageOut(BaseModel):
    id: str
    role: str
    content: str
    timestamp: datetime

    class Config:
        orm_mode = True

class ConversationOut(BaseModel):
    id: str
    user_id: Optional[str]
    mode: str
    title: Optional[str]
    updated_at: datetime

    class Config:
        orm_mode = True

class ConversationDetail(BaseModel):
    id: str
    user_id: Optional[str]
    mode: str
    title: Optional[str]
    summary: Optional[str]
    messages: List[MessageOut]

    class Config:
        orm_mode = True
