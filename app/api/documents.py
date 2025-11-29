"""
Document API endpoints for RAG
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.document import DocumentCreate, DocumentResponse
from app.models import Document, Conversation
from app.services.rag_service import RAGService
from app.utils.error_handler import DocumentNotFoundError, ConversationNotFoundError

router = APIRouter(prefix="/api/v1/documents", tags=["documents"])
rag_service = RAGService()


@router.post("", response_model=DocumentResponse, status_code=201)
def create_document(
    document_data: DocumentCreate,
    db: Session = Depends(get_db)
):
    """
    Upload a document for RAG
    
    - **title**: Document title
    - **content**: Document content
    """
    # Chunk the document
    chunks = rag_service.chunk_document(document_data.content)
    
    # Create document
    document = Document(
        title=document_data.title,
        content=document_data.content,
        chunks=chunks
    )
    db.add(document)
    db.commit()
    db.refresh(document)
    
    return DocumentResponse(
        id=document.id,
        title=document.title,
        created_at=document.created_at,
        chunk_count=len(chunks) if chunks else 0
    )


@router.post("/conversations/{conversation_id}/documents/{document_id}", status_code=200)
def attach_document_to_conversation(
    conversation_id: int,
    document_id: int,
    db: Session = Depends(get_db)
):
    """
    Attach a document to a conversation for RAG
    
    - **conversation_id**: Conversation ID
    - **document_id**: Document ID
    """
    # Get conversation
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id
    ).first()
    if not conversation:
        raise ConversationNotFoundError(conversation_id)
    
    # Get document
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise DocumentNotFoundError(document_id)
    
    # Attach document
    if document not in conversation.documents:
        conversation.documents.append(document)
        db.commit()
    
    return {"message": "Document attached successfully"}
