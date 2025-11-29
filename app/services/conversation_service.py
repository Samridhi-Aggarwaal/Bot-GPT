"""
Conversation Service - Business logic for conversation management
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models import Conversation, Message, User, Document
from app.schemas.conversation import ConversationCreate
from app.services.llm_service import LLMService
from app.services.rag_service import RAGService
from app.utils.error_handler import ConversationNotFoundError, DocumentNotFoundError


class ConversationService:
    """Service for conversation business logic"""
    
    def __init__(self):
        """Initialize services"""
        self.llm_service = LLMService()
        self.rag_service = RAGService()
    
    def create_conversation(
        self,
        db: Session,
        conversation_data: ConversationCreate
    ) -> Conversation:
        """
        Create new conversation with first message
        
        Args:
            db: Database session
            conversation_data: Conversation creation data
        
        Returns:
            Created conversation with messages
        """
        # Ensure user exists (create if not)
        user = db.query(User).filter(User.id == conversation_data.user_id).first()
        if not user:
            # Create default user for demo purposes
            user = User(
                id=conversation_data.user_id,
                username=f"user_{conversation_data.user_id}",
                email=f"user_{conversation_data.user_id}@example.com"
            )
            db.add(user)
            db.commit()
        
        # Generate title from first message
        title = self.llm_service.generate_title(conversation_data.first_message)
        
        # Create conversation
        conversation = Conversation(
            user_id=conversation_data.user_id,
            title=title,
            mode=conversation_data.mode
        )
        db.add(conversation)
        db.flush()  # Get conversation ID
        
        # Attach documents if in RAG mode
        if conversation_data.mode == "rag" and conversation_data.document_ids:
            for doc_id in conversation_data.document_ids:
                document = db.query(Document).filter(Document.id == doc_id).first()
                if document:
                    conversation.documents.append(document)
        
        # Create user message
        user_message = Message(
            conversation_id=conversation.id,
            role="user",
            content=conversation_data.first_message
        )
        db.add(user_message)
        
        # Generate assistant response
        assistant_content, tokens = self._generate_response(
            db, conversation, conversation_data.first_message
        )
        
        # Create assistant message
        assistant_message = Message(
            conversation_id=conversation.id,
            role="assistant",
            content=assistant_content,
            tokens_used=tokens
        )
        db.add(assistant_message)
        
        db.commit()
        db.refresh(conversation)
        
        return conversation
    
    def add_message(
        self,
        db: Session,
        conversation_id: int,
        content: str
    ) -> tuple[Message, Message]:
        """
        Add user message and generate assistant response
        
        Args:
            db: Database session
            conversation_id: Conversation ID
            content: User message content
        
        Returns:
            Tuple of (user_message, assistant_message)
        """
        # Get conversation
        conversation = db.query(Conversation).filter(
            Conversation.id == conversation_id
        ).first()
        
        if not conversation:
            raise ConversationNotFoundError(conversation_id)
        
        # Create user message
        user_message = Message(
            conversation_id=conversation_id,
            role="user",
            content=content
        )
        db.add(user_message)
        
        # Generate assistant response
        assistant_content, tokens = self._generate_response(db, conversation, content)
        
        # Create assistant message
        assistant_message = Message(
            conversation_id=conversation_id,
            role="assistant",
            content=assistant_content,
            tokens_used=tokens
        )
        db.add(assistant_message)
        
        db.commit()
        db.refresh(user_message)
        db.refresh(assistant_message)
        
        return user_message, assistant_message
    
    def _generate_response(
        self,
        db: Session,
        conversation: Conversation,
        user_message: str
    ) -> tuple[str, int]:
        """
        Generate LLM response based on conversation mode
        
        Args:
            db: Database session
            conversation: Conversation object
            user_message: Current user message
        
        Returns:
            Tuple of (response_content, tokens_used)
        """
        # Get conversation history
        messages = [
            {"role": msg.role, "content": msg.content}
            for msg in conversation.messages
        ]
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        # Generate response based on mode
        if conversation.mode == "rag" and conversation.documents:
            # RAG mode: retrieve relevant chunks
            all_chunks = []
            for document in conversation.documents:
                if document.chunks:
                    all_chunks.extend(document.chunks)
            
            if all_chunks:
                # Retrieve relevant chunks
                relevant_chunks = self.rag_service.retrieve_relevant_chunks(
                    user_message, all_chunks
                )
                
                # Build RAG prompt
                system_prompt = self.rag_service.build_rag_prompt(
                    user_message, relevant_chunks
                )
            else:
                system_prompt = "You are a helpful AI assistant."
        else:
            # Open mode: standard prompt
            system_prompt = "You are a helpful AI assistant."
        
        # Generate response
        response, tokens = self.llm_service.generate_response(
            messages, system_prompt
        )
        
        return response, tokens
    
    def get_conversation(self, db: Session, conversation_id: int) -> Conversation:
        """Get conversation by ID"""
        conversation = db.query(Conversation).filter(
            Conversation.id == conversation_id
        ).first()
        
        if not conversation:
            raise ConversationNotFoundError(conversation_id)
        
        return conversation
    
    def list_conversations(
        self,
        db: Session,
        user_id: int,
        skip: int = 0,
        limit: int = 20
    ) -> tuple[List[Conversation], int]:
        """
        List conversations for a user with pagination
        
        Returns:
            Tuple of (conversations, total_count)
        """
        query = db.query(Conversation).filter(Conversation.user_id == user_id)
        total = query.count()
        conversations = query.order_by(
            Conversation.updated_at.desc()
        ).offset(skip).limit(limit).all()
        
        return conversations, total
    
    def delete_conversation(self, db: Session, conversation_id: int):
        """Delete conversation and all messages"""
        conversation = db.query(Conversation).filter(
            Conversation.id == conversation_id
        ).first()
        
        if not conversation:
            raise ConversationNotFoundError(conversation_id)
        
        db.delete(conversation)
        db.commit()
