
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
from unittest.mock import patch


def test_ask_endpoint_returns_answer_and_evidence():
    expected = {
        "status": "answered",
        "answer": "Test answer",
        "confidence": "Medium",
        "evidence": [{"source": "test.pdf"}],
    }

    with patch("app.main.answer_ceo_question", return_value=expected) as mocked:
        response = client.post(
            "/api/ask",
            json={"question": "Why was engineering hiring paused?"}
        )

    assert response.status_code == 200
    assert response.json() == expected
    mocked.assert_called_once_with(
        "Why was engineering hiring paused?"
    )


def test_ask_endpoint_rejects_blank_question():
    response = client.post(
        "/api/ask",
        json={"question": "   "}
    )

    assert response.status_code == 422


def test_ask_endpoint_rejects_question_over_1000_characters():
    response = client.post(
        "/api/ask",
        json={"question": "a" * 1001}
    )

    assert response.status_code == 422


def test_ask_endpoint_preserves_privacy_refusal():
    response = client.post(
        "/api/ask",
        json={"question": "What is Rahul's salary?"}
    )

    assert response.status_code == 200
    assert response.json()["status"] == "refused"
    assert response.json()["evidence"] == []


def test_ask_endpoint_handles_unsupported_question():
    response = client.post(
        "/api/ask",
        json={"question": "What is the CEO's favorite color?"}
    )

    assert response.status_code == 200
    assert response.json()["status"] == "insufficient_evidence"
    assert response.json()["evidence"] == []


def test_ask_endpoint_handles_answer_engine_failure():
    with patch(
        "app.main.answer_ceo_question",
        side_effect=RuntimeError("Simulated answer failure")
    ):
        response = client.post(
            "/api/ask",
            json={"question": "What is the monthly burn?"}
        )

    assert response.status_code == 500
    assert response.json()["detail"] == "Unable to answer CEO question"
