"""
Test conversation service
"""
import pytest
from app.services.conversation_service import ConversationService


def test_conversation_service_initialization():
    """Test that conversation service initializes correctly"""
    service = ConversationService()
    assert service.llm_service is not None
    assert service.rag_service is not None


def test_llm_service_title_generation():
    """Test title generation from first message"""
    service = ConversationService()
    
    # Short message
    title = service.llm_service.generate_title("Hello")
    assert title == "Hello"
    
    # Long message
    long_message = "This is a very long message that exceeds fifty characters and should be truncated"
    title = service.llm_service.generate_title(long_message)
    assert len(title) <= 53  # 50 chars + "..."
    assert title.endswith("...")
