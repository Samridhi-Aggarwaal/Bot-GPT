# AI Chatbot Backend (FastAPI + RAG + LLM Integration)

A fully modular, production-ready backend for an AI-powered chatbot system.
Built with FastAPI, featuring conversation management, document ingestion, Retrieval-Augmented Generation (RAG), and a clean service-driven architecture.

## Overview
This repository contains a minimal FastAPI-based backend for the BOT-GPT case study.
It supports:
- Multi-turn conversations (create, list, retrieve, delete)
- Add messages which trigger LLM responses (mock by default)
- Document upload and simple RAG chunking + naive retrieval
- SQLite persistence (file: bot_gpt.db)
- Dockerfile and docker-compose for easy running
- Basic pytest tests

## 🚀 Features
🗨️ Conversation Management
- Create and manage chat sessions.
- Store message history using SQLAlchemy.
- Extensible architecture for analytics or chat memory.
  
📚 Retrieval-Augmented Generation (RAG)
- Upload and index documents.
- Retrieve relevant context chunks using vector similarity.
- Seamlessly integrates retrieved context into LLM responses.
  
🤖 LLM Service Layer
- Plug-and-play support for different LLM providers.
- Clean interface to integrate OpenAI, Anthropic, or local models.

🐳 Fully Dockerized
- Dockerfile included for production builds.
- docker-compose.yml for quick development deployment.

🧪 Test Suite
- Pytest-based tests for conversation creation and RAG functions.
- Centralised prompt and response management.

## 🛠️ Tech Stack
- FastAPI
- Python 3.10+
- SQLAlchemy
- Docker & Docker Compose
- Pytest
- (Optional) OpenAI / Anthropic / Local LLMs

## 🚀 Quick Start (local)

### Prerequisites

- Python 3.11+
- Docker & Docker Compose (optional)
- Groq API Key ([Get one free here](https://console.groq.com))

### Local Setup
1. **Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment**
```bash
cp .env.example .env
# Edit and add your GROQ_API_KEY
```

4. **Run the application**
```bash
uvicorn app.main:app --reload
```

### Docker Setup

1. **Configure environment**
```bash
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

2. **Start services**
```bash
docker-compose up
```

## 📚 API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc


## 💡 Key Design Decisions

### 1. **Tech Stack**
- **FastAPI**: Modern, fast, with automatic API documentation
- **SQLAlchemy**: Flexible ORM supporting multiple databases
- **Groq API**: Free tier with fast Llama 3 inference
- **Pydantic**: Data validation and settings management

### 2. **Context Management**
- **Sliding Window**: Keeps recent messages within token limits
- **Token Counting**: Uses tiktoken for accurate token estimation
- **System Prompts**: Optimized for clarity and token efficiency

### 3. **RAG Implementation**
- **Simple Chunking**: Word-based with configurable overlap
- **Keyword Retrieval**: TF-IDF style matching (no vector DB required)
- **Context Injection**: Retrieved chunks added to system prompt

### 4. **Error Handling**
- **Retry Logic**: Exponential backoff for API failures
- **Custom Exceptions**: Clear error messages for debugging
- **Graceful Degradation**: Fallback responses when LLM unavailable

### 5. **Scalability**
- **Stateless Design**: Easy horizontal scaling
- **Database Indexing**: Optimized queries for user_id and timestamps
- **Connection Pooling**: Efficient database connections


## 🔐 Security Notes

For production deployment:
- Use environment variables for secrets
- Enable HTTPS/TLS
- Implement authentication (JWT, OAuth)
- Rate limiting on API endpoints
- Input validation and sanitization
- CORS configuration for specific origins


---
