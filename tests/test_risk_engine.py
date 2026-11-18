
import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[1] / "backend"
sys.path.insert(0, str(BACKEND_DIR))

from app.cockpit.risk_engine import (
    build_risk,
    get_top_risks,
    collect_evidence,
)


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


def test_engineering_risk_includes_day3_records():
    risks = get_top_risks()
    engineering = risks[0]

    evidence_text = " ".join(
        item["evidence"] for item in engineering["evidence"]
    )

    assert "2026-12-15" in evidence_text

    assert all(
        incident in evidence_text
        for incident in ["INC-201", "INC-203", "INC-205"]
    )


def test_collect_evidence_requires_all_terms(monkeypatch):
    import app.cockpit.risk_engine as risk_engine

    monkeypatch.setattr(
        risk_engine,
        "search_evidence",
        lambda *args, **kwargs: [
            {
                "source_file": "Incidents_Aug-Oct_2026.xlsx",
                "text": "INC-201 SEV1 routing-api",
                "citation": "Incidents_Aug-Oct_2026.xlsx (row 1, Day3)",
            },
            {
                "source_file": "Incidents_Aug-Oct_2026.xlsx",
                "text": "INC-203 SEV1 database",
                "citation": "Incidents_Aug-Oct_2026.xlsx (row 2, Day3)",
            },
        ],
    )

    results = collect_evidence(
        query="incident",
        allowed_sources=["Incidents_Aug-Oct_2026.xlsx"],
        required_terms=["SEV1", "routing-api"],
    )

    assert len(results) == 1
    assert "INC-201" in results[0]["evidence"]
