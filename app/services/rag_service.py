"""
RAG Service - Document retrieval and context augmentation
"""
import re
from typing import List, Dict
from collections import Counter
from app.config import settings


class RAGService:
    """Service for Retrieval-Augmented Generation"""
    
    def __init__(self):
        """Initialize RAG service"""
        self.chunk_size = settings.CHUNK_SIZE
        self.chunk_overlap = settings.CHUNK_OVERLAP
        self.top_k = settings.TOP_K_CHUNKS
    
    def chunk_document(self, content: str) -> List[Dict[str, str]]:
        """
        Split document into chunks with overlap
        
        Args:
            content: Document content
        
        Returns:
            List of chunk dicts with 'text' and 'index'
        """
        # Simple word-based chunking
        words = content.split()
        chunks = []
        
        i = 0
        chunk_index = 0
        while i < len(words):
            # Get chunk of words
            chunk_words = words[i:i + self.chunk_size]
            chunk_text = " ".join(chunk_words)
            
            chunks.append({
                "index": chunk_index,
                "text": chunk_text
            })
            
            # Move forward with overlap
            i += self.chunk_size - self.chunk_overlap
            chunk_index += 1
        
        return chunks
    
    def retrieve_relevant_chunks(
        self,
        query: str,
        chunks: List[Dict[str, str]]
    ) -> List[str]:
        """
        Retrieve most relevant chunks using keyword matching
        
        Args:
            query: User query
            chunks: List of document chunks
        
        Returns:
            List of top-K relevant chunk texts
        """
        # Extract keywords from query (simple approach)
        query_keywords = self._extract_keywords(query)
        
        # Score each chunk
        chunk_scores = []
        for chunk in chunks:
            score = self._calculate_relevance_score(query_keywords, chunk["text"])
            chunk_scores.append((chunk["text"], score))
        
        # Sort by score and get top-K
        chunk_scores.sort(key=lambda x: x[1], reverse=True)
        top_chunks = [text for text, score in chunk_scores[:self.top_k]]
        
        return top_chunks
    
    def _extract_keywords(self, text: str) -> List[str]:
        """
        Extract keywords from text (simple approach)
        
        Args:
            text: Input text
        
        Returns:
            List of keywords
        """
        # Convert to lowercase and remove punctuation
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)
        
        # Split into words
        words = text.split()
        
        # Remove common stop words (simple list)
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
            'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
            'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that',
            'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they'
        }
        
        keywords = [word for word in words if word not in stop_words and len(word) > 2]
        return keywords
    
    def _calculate_relevance_score(self, keywords: List[str], chunk: str) -> float:
        """
        Calculate relevance score using keyword matching
        
        Args:
            keywords: List of query keywords
            chunk: Chunk text
        
        Returns:
            Relevance score
        """
        chunk_lower = chunk.lower()
        
        # Count keyword occurrences
        score = 0
        for keyword in keywords:
            score += chunk_lower.count(keyword)
        
        return score
    
    def build_rag_prompt(self, query: str, retrieved_chunks: List[str]) -> str:
        """
        Build system prompt with retrieved context
        
        Args:
            query: User query
            retrieved_chunks: Retrieved document chunks
        
        Returns:
            System prompt with context
        """
        context = "\n\n".join(retrieved_chunks)
        
        prompt = f"""You are a helpful AI assistant. Answer the user's question based on the following context from the provided documents.

Context:
{context}

Instructions:
- Answer the question using information from the context above
- If the answer is not in the context, clearly state that you don't have enough information
- Be concise and accurate
- Cite specific parts of the context when relevant"""
        
        return prompt
