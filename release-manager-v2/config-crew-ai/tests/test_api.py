import os
os.environ["OPENAI_API_KEY"] = "ollama"
os.environ["OPENAI_API_BASE"] = "http://localhost:11434/v1"
os.environ["OPENAI_MODEL_NAME"] = "qwen2.5"

from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app

client = TestClient(app)

def test_merge_config_endpoint_success():
    # Mock CrewAI kickoff
    with patch("src.main.Crew.kickoff") as mock_kickoff:
        mock_kickoff.return_value = "Mocked CrewAI Result"
        
        payload = {
            "ticket_id": "PROJ-123",
            "config_test_content": "{}",
            "config_pre_current": "{}",
            "config_pro_current": "{}"
        }
        
        response = client.post("/api/v1/config/merge", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "Mocked CrewAI Result" in data["reasoning"]

def test_merge_config_invalid_payload():
    response = client.post("/api/v1/config/merge", json={"invalid": "data"})
    assert response.status_code == 422 # Unprocessable Entity
