from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)

def test_upload_document_and_retrieve():
    payload = {"user_id":"user_test2","first_message":"Start RAG","mode":"rag"}
    r = client.post("/conversations", json=payload)
    conv_id = r.json()["conversation_id"]
    # upload "document"
    files = {'file': ('doc.txt', 'This is a test document about Python. Python is great.')}
    r2 = client.post(f"/conversations/{conv_id}/documents/upload", files=files)
    assert r2.status_code == 200
    body = r2.json()
    assert "document_id" in body
