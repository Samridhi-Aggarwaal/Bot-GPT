"""
LLM Service - Integration with Groq API
"""
import time
from typing import List, Dict, Optional
from groq import Groq
from app.config import settings
from app.utils.context_manager import count_tokens, build_context_window
from app.utils.error_handler import LLMAPIError


class LLMService:
    """Service for interacting with LLM APIs"""
    
    def __init__(self):
        """Initialize Groq client"""
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = settings.LLM_MODEL
        self.max_retries = 3
        self.retry_delay = 1  # seconds
    
    def generate_response(
        self,
        messages: List[Dict[str, str]],
        system_prompt: str = "You are a helpful AI assistant.",
        max_tokens: int = 1000
    ) -> tuple[str, int]:
        """
        Generate response from LLM
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            system_prompt: System prompt for the LLM
            max_tokens: Maximum tokens in response
        
        Returns:
            Tuple of (response_text, tokens_used)
        
        Raises:
            LLMAPIError: If API call fails after retries
        """
        # Build context window with token management
        context = build_context_window(messages, system_prompt)
        
        # Retry logic with exponential backoff
        for attempt in range(self.max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=context,
                    max_tokens=max_tokens,
                    temperature=0.7
                )
                
                # Extract response and token usage
                assistant_message = response.choices[0].message.content
                tokens_used = response.usage.total_tokens
                
                return assistant_message, tokens_used
                
            except Exception as e:
                if attempt < self.max_retries - 1:
                    # Exponential backoff
                    wait_time = self.retry_delay * (2 ** attempt)
                    time.sleep(wait_time)
                    continue
                else:
                    # Final attempt failed
                    raise LLMAPIError(f"LLM API failed after {self.max_retries} attempts: {str(e)}")
    
    def generate_title(self, first_message: str) -> str:
        """
        Generate a conversation title from the first message
        
        Args:
            first_message: First user message
        
        Returns:
            Generated title (truncated to 50 chars)
        """
        # Simple heuristic: use first 50 chars of message
        title = first_message[:50]
        if len(first_message) > 50:
            title += "..."
        return title
