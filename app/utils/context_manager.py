"""
Context management utilities for handling LLM token limits
"""
import tiktoken
from typing import List, Dict
from app.config import settings


def count_tokens(text: str, model: str = "gpt-3.5-turbo") -> int:
    """
    Count tokens in a text string using tiktoken
    
    Args:
        text: Text to count tokens for
        model: Model name for tokenizer (default: gpt-3.5-turbo)
    
    Returns:
        Number of tokens
    """
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        # Fallback to cl100k_base encoding for unknown models
        encoding = tiktoken.get_encoding("cl100k_base")
    
    return len(encoding.encode(text))


def build_context_window(
    messages: List[Dict[str, str]],
    system_prompt: str,
    max_tokens: int = None
) -> List[Dict[str, str]]:
    """
    Build context window with sliding window strategy
    
    Keeps the most recent messages that fit within token budget.
    Always includes system prompt.
    
    Args:
        messages: List of message dicts with 'role' and 'content'
        system_prompt: System prompt to always include
        max_tokens: Maximum tokens allowed (default from settings)
    
    Returns:
        List of messages that fit within token budget
    """
    if max_tokens is None:
        max_tokens = settings.MAX_CONTEXT_TOKENS
    
    # Start with system prompt
    context = [{"role": "system", "content": system_prompt}]
    total_tokens = count_tokens(system_prompt)
    
    # Add messages from newest to oldest
    for msg in reversed(messages):
        msg_tokens = count_tokens(msg["content"])
        
        # Check if adding this message would exceed limit
        if total_tokens + msg_tokens > max_tokens:
            break
        
        # Insert after system prompt (to maintain chronological order)
        context.insert(1, msg)
        total_tokens += msg_tokens
    
    return context


def truncate_context(
    messages: List[Dict[str, str]],
    max_messages: int = None
) -> List[Dict[str, str]]:
    """
    Truncate context to keep only the last N messages
    
    Args:
        messages: List of message dicts
        max_messages: Maximum number of messages to keep
    
    Returns:
        Truncated list of messages
    """
    if max_messages is None:
        max_messages = settings.SLIDING_WINDOW_SIZE
    
    if len(messages) <= max_messages:
        return messages
    
    return messages[-max_messages:]
