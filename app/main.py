from fastapi import FastAPI
from app.api import conversations, documents
from app.db.database import init_db

app = FastAPI(title="BOT GPT Backend")

app.include_router(conversations.router, prefix="/conversations", tags=["conversations"])
app.include_router(documents.router, prefix="/conversations/{conversation_id}/documents", tags=["documents"])

@app.on_event("startup")
def startup():
    init_db()
