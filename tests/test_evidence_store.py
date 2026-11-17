
import sys
from pathlib import Path

BACKEND_APP = Path(__file__).resolve().parents[1] / "backend" / "app"
sys.path.insert(0, str(BACKEND_APP))

from rag.evidence_store import (
    normalize_document,
    build_evidence_store,
)


def make_record(content, file_type=".txt", status="success"):
    return {
        "source_file": "sample.txt",
        "source_path": "data/raw/sample.txt",
        "release_day": "Day1",
        "file_type": file_type,
        "content": content,
        "status": status,
    }


def test_string_content_becomes_one_evidence_record():
    record = make_record("Company ARR is Rs. 6.1 Cr.")

    result = normalize_document(record)

    assert len(result) == 1
    assert result[0]["text"] == "Company ARR is Rs. 6.1 Cr."
    assert result[0]["locator"] == "document"


def test_pdf_pages_become_separate_evidence_records():
    record = make_record([
        {"page": 1, "text": "First page"},
        {"page": 2, "text": "Second page"},
    ], ".pdf")

    result = normalize_document(record)

    assert len(result) == 2
    assert result[0]["locator"] == "page-1"
    assert result[1]["locator"] == "page-2"


def test_excel_rows_become_separate_evidence_records():
    record = make_record({
        "Payroll": [
            {"Employee": "A", "Amount": 100},
            {"Employee": "B", "Amount": 200},
        ]
    }, ".xlsx")

    result = normalize_document(record)

    assert len(result) == 2
    assert "Employee: A" in result[0]["text"]
    assert "Amount: 200" in result[1]["text"]
    assert "sheet-Payroll-row-1" == result[0]["locator"]


def test_empty_excel_rows_are_skipped():
    record = make_record({
        "Sheet1": [
            {"Employee": None, "Amount": None},
            {"Employee": "A", "Amount": 100},
        ]
    }, ".xlsx")

    result = normalize_document(record)

    assert len(result) == 1


def test_failed_documents_are_not_normalized():
    record = make_record("Some content", status="failed")

    assert normalize_document(record) == []


def test_source_metadata_is_preserved():
    record = make_record("Evidence text")

    result = normalize_document(record)
    item = result[0]

    assert item["source_file"] == "sample.txt"
    assert item["source_path"] == "data/raw/sample.txt"
    assert item["release_day"] == "Day1"
    assert item["file_type"] == ".txt"


def test_all_evidence_ids_are_unique():
    evidence = build_evidence_store()
    ids = [item["evidence_id"] for item in evidence]

    assert len(ids) == len(set(ids))


def test_all_evidence_records_have_nonempty_text():
    evidence = build_evidence_store()

    assert all(
        isinstance(item["text"], str) and item["text"].strip()
        for item in evidence
    )


def test_day1_and_day2_evidence_are_loaded():
    evidence = build_evidence_store()
    release_days = {item["release_day"] for item in evidence}

    assert {"Day1", "Day2"}.issubset(release_days)
