
import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[1] / "backend"
sys.path.insert(0, str(BACKEND_DIR))

from app.cockpit.risk_engine import build_risk, get_top_risks


def test_returns_three_risks():
    risks = get_top_risks()

    assert len(risks) == 3


def test_risks_are_ranked_by_score():
    risks = get_top_risks()

    scores = [risk["score"] for risk in risks]

    assert scores == sorted(scores, reverse=True)


def test_priorities_follow_rank_order():
    risks = get_top_risks()

    priorities = [risk["priority"] for risk in risks]

    assert priorities == [1, 2, 3]


def test_each_risk_has_evidence():
    risks = get_top_risks()

    for risk in risks:
        assert len(risk["evidence"]) > 0


def test_payroll_register_is_not_exposed():
    risks = get_top_risks()

    for risk in risks:
        for item in risk["evidence"]:
            assert "Payroll_Register" not in item["source"]


def test_risk_score_calculation():
    risk = build_risk(
        risk_id="TEST-001",
        title="Test risk",
        confidence="Medium",
        impact="High",
        urgency=4,
        explanation="Test explanation",
        action="Test action",
        evidence=[
            {"source": "source_a.pdf"},
            {"source": "source_b.pdf"}
        ],
        uncertainty="Test uncertainty"
    )

    # High impact = 3 * 3 = 9
    # Urgency = 4 * 2 = 8
    # Two distinct sources = 2
    assert risk["score"] == 19
