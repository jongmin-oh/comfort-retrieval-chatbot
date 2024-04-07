from fastapi.testclient import TestClient
from manage import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    

def test_chatbot():
    response = client.post("/chatbot/respond", json={"query": "안녕"})
    assert response.status_code == 200