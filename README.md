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

## Quickstart (local)
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API docs: http://localhost:8000/docs

## Run tests
```
pytest -q
```

## LLM Integration
By default, the server uses a mock LLM adapter that echoes user input. To integrate a real provider, set the environment variable `LLM_PROVIDER` and implement provider logic in `app/services/llm_service.py`.

## RAG
Upload documents via:
    POST /conversations/{conversation_id}/documents/upload
Provide a text file; the service will chunk and store it for naive retrieval.

## Docker
Build & run:
```
docker build -t bot-gpt-backend
docker run -p 8000:8000 bot-gpt-backend
```
Or with docker-compose:
```
docker-compose up --build
```
