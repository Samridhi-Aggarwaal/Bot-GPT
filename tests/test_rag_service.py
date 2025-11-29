"""
Test RAG service
"""
import pytest
from app.services.rag_service import RAGService


def test_rag_service_initialization():
    """Test RAG service initialization"""
    service = RAGService()
    assert service.chunk_size > 0
    assert service.chunk_overlap >= 0
    assert service.top_k > 0


def test_document_chunking():
    """Test document chunking"""
    service = RAGService()
    
    # Create a test document
    content = " ".join([f"word{i}" for i in range(1000)])
    
    # Chunk the document
    chunks = service.chunk_document(content)
    
    # Verify chunks were created
    assert len(chunks) > 0
    assert all("text" in chunk for chunk in chunks)
    assert all("index" in chunk for chunk in chunks)


def test_keyword_extraction():
    """Test keyword extraction"""
    service = RAGService()
    
    text = "What is machine learning and how does it work?"
    keywords = service._extract_keywords(text)
    
    # Should extract meaningful keywords
    assert "machine" in keywords
    assert "learning" in keywords
    assert "work" in keywords
    
    # Should filter out stop words
    assert "what" not in keywords
    assert "is" not in keywords
    assert "and" not in keywords


def test_chunk_retrieval():
    """Test retrieving relevant chunks"""
    service = RAGService()
    
    # Create test chunks
    chunks = [
        {"index": 0, "text": "Machine learning is a subset of artificial intelligence"},
        {"index": 1, "text": "Python is a popular programming language"},
        {"index": 2, "text": "Neural networks are used in deep learning"}
    ]
    
    # Query about machine learning
    query = "What is machine learning?"
    relevant_chunks = service.retrieve_relevant_chunks(query, chunks)
    
    # Should retrieve chunks
    assert len(relevant_chunks) > 0
    # First chunk should be most relevant
    assert "machine learning" in relevant_chunks[0].lower()
