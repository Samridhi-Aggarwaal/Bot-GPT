"""
Configuration management using Pydantic Settings
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    
    # Database
    DATABASE_URL: str = "sqlite:///./botgpt.db"
    
    # LLM API
    GROQ_API_KEY: str
    LLM_MODEL: str = "llama3-8b-8192"
    MAX_TOKENS: int = 4000
    
    # Application
    APP_NAME: str = "BOT GPT"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Context Management
    MAX_CONTEXT_TOKENS: int = 4000
    SLIDING_WINDOW_SIZE: int = 10
    
    # RAG Settings
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 50
    TOP_K_CHUNKS: int = 3
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
