"""
Error handling utilities
"""
from fastapi import HTTPException, status


class ConversationNotFoundError(HTTPException):
    """Raised when conversation is not found"""
    def __init__(self, conversation_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Conversation with id {conversation_id} not found"
        )


class DocumentNotFoundError(HTTPException):
    """Raised when document is not found"""
    def __init__(self, document_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document with id {document_id} not found"
        )


class LLMAPIError(HTTPException):
    """Raised when LLM API call fails"""
    def __init__(self, message: str = "LLM API request failed"):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=message
        )


class InvalidModeError(HTTPException):
    """Raised when invalid conversation mode is specified"""
    def __init__(self, mode: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid conversation mode: {mode}. Must be 'open' or 'rag'"
        )
