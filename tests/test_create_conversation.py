from fastapi.testclient import TestClient
from app.main import app
import os
client = TestClient(app)

def test_create_and_get_conversation():
    payload = {"user_id":"user_test","first_message":"Hello BOT","mode":"open"}
    r = client.post("/conversations", json=payload)
    assert r.status_code == 201
    conv_id = r.json()["conversation_id"]
    # add message
    r2 = client.post(f"/conversations/{conv_id}/messages", json={"content":"How are you?"})
    assert r2.status_code == 200
    assert "assistant_message" in r2.json()
    # get conversation
    r3 = client.get(f"/conversations/{conv_id}")
    assert r3.status_code == 200
    data = r3.json()
    assert data["id"] == conv_id
    assert len(data["messages"]) >= 2
