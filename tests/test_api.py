
import sys
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient

BACKEND_DIR = Path(__file__).resolve().parents[1] / "backend"
sys.path.insert(0, str(BACKEND_DIR))

from app.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_risk_endpoint_returns_three_risks():
    response = client.get("/api/risks")

    assert response.status_code == 200

    data = response.json()

    assert data["count"] == 3
    assert len(data["risks"]) == 3


def test_risk_endpoint_contains_required_fields():
    response = client.get("/api/risks")

    assert response.status_code == 200

    for risk in response.json()["risks"]:
        assert risk["title"]
        assert risk["confidence"]
        assert risk["impact"]
        assert risk["recommended_action"]
        assert "evidence" in risk
        assert "uncertainty" in risk


def test_api_handles_risk_engine_failure():
    with patch(
        "app.main.get_top_risks",
        side_effect=RuntimeError("Simulated retrieval failure")
    ):
        response = client.get("/api/risks")

    assert response.status_code == 500
    assert "Unable to generate risk summary" in response.json()["detail"]
