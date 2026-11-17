
import sys
from pathlib import Path

BACKEND_APP = Path(__file__).resolve().parents[1] / "backend" / "app"
sys.path.insert(0, str(BACKEND_APP))

from rag.retriever import search_evidence


def test_latest_burn_ranks_latest_board_update_first():
    results = search_evidence(
        "What is the latest monthly burn?",
        release_days=["Day1", "Day2"],
        top_k=10
    )

    board_results = [
        item for item in results
        if "Board_Update" in item["source_file"]
    ]

    assert len(board_results) >= 2

    assert "Jul-Sep_2026" in board_results[0]["source_file"]
    assert board_results[0]["score"] > board_results[1]["score"]


def test_hiring_pause_finds_both_paused_roles():
    results = search_evidence(
        "Why were engineering hiring roles paused?",
        release_days=["Day1", "Day2"],
        top_k=20
    )

    combined_text = " ".join(item["text"] for item in results)

    assert "REQ-014" in combined_text
    assert "REQ-015" in combined_text


def test_engineering_pulse_finds_latest_score():
    results = search_evidence(
        "What happened to the engineering pulse score?",
        release_days=["Day1", "Day2"],
        top_k=30
    )

    combined_text = " ".join(item["text"] for item in results)

    assert "3.1" in combined_text


def test_siddharth_resignation_finds_original_letter():
    results = search_evidence(
        "Why did Siddharth resign?",
        release_days=["Day1", "Day2"],
        top_k=10
    )

    assert any(
        item["source_file"] == "Resignation_Letter_SM.pdf"
        for item in results
    )


def test_empty_query_returns_no_results():
    results = search_evidence("   ")

    assert results == []


def test_irrelevant_query_does_not_return_random_evidence():
    results = search_evidence(
        "What is the weather on Mars?",
        release_days=["Day1", "Day2"]
    )

    assert results == []

def test_payroll_records_never_appear_in_general_search():
    results = search_evidence(
        "Why did Siddharth resign?",
        release_days=["Day1", "Day2"],
        top_k=30
    )

    assert all(
        "Payroll" not in item["source_file"]
        for item in results
    )