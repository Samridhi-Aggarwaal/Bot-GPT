import os
import time
# Simple pluggable LLM adapter.
# By default it returns a mocked response to avoid external API calls.
# To integrate with a real provider, set LLM_PROVIDER env var and provide API keys.

LLM_PROVIDER = os.getenv("LLM_PROVIDER","mock")

def generate_response(context: dict, user_message: str, conversation_id: str):
    if LLM_PROVIDER == "mock":
        # simple deterministic mock
        resp = f"Echo: {user_message}"
        meta = {"provider": "mock", "tokens": len(user_message.split())}
        return resp, meta
    # Placeholder for real provider integration
    # Example: call HuggingFace/Groq API here
    start = time.time()
    resp = f"[LLM:{LLM_PROVIDER}] {user_message}"
    meta = {"provider": LLM_PROVIDER, "latency_ms": int((time.time()-start)*1000)}
    return resp, meta
