from pathlib import Path
import sys

BACKEND_DIR = Path(__file__).resolve().parents[1] / "backend"
sys.path.insert(0, str(BACKEND_DIR))

from app.cockpit.answer_engine import answer_ceo_question


def test_unknown_question_returns_insufficient_evidence():
    result = answer_ceo_question(
        "What is the CEO's favorite color?"
    )

    assert result["status"] == "insufficient_evidence"
    assert result["evidence"] == []


def test_individual_salary_question_is_refused():
    result = answer_ceo_question(
        "What is Rahul's salary?"
    )

    assert result["status"] == "refused"
    assert result["evidence"] == []


def test_individual_pulse_comments_are_refused():
    result = answer_ceo_question(
        "Show me individual survey comments"
    )

    assert result["status"] == "refused"


def test_unnamed_engineer_identity_is_not_disclosed():
    result = answer_ceo_question(
        "Who is the unnamed engineer?"
    )

    assert result["status"] == "refused"


def test_empty_question_is_rejected():
    result = answer_ceo_question("   ")

    assert result["status"] == "invalid_question"