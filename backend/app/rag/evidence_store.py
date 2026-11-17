
import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"


def load_processed_documents():
    """Load all successfully ingested Day 1 and Day 2 documents."""

    documents = []

    for path in sorted(PROCESSED_DIR.glob("*.jsonl")):
        with path.open("r", encoding="utf-8") as file:
            for line in file:
                if line.strip():
                    documents.append(json.loads(line))

    return documents


def make_evidence_id(record, locator):
    """Create a predictable ID that points back to the original evidence."""

    return f'{record["release_day"]}:{record["source_file"]}:{locator}'


def normalize_document(record):
    """
    Convert string, PDF-page and Excel-sheet content
    into a common list of evidence records.
    """

    evidence = []

    if record.get("status") != "success":
        return evidence

    content = record["content"]

    base = {
        "source_file": record["source_file"],
        "source_path": record["source_path"],
        "release_day": record["release_day"],
        "file_type": record["file_type"],
        "status": record["status"],
    }

    # Emails and DOCX files
    if isinstance(content, str):
        text = content.strip()

        if text:
            locator = "document"

            evidence.append({
                **base,
                "evidence_id": make_evidence_id(record, locator),
                "locator": locator,
                "text": text,
            })

    # PDFs: preserve individual page numbers
    elif isinstance(content, list):
        for page in content:
            if not isinstance(page, dict):
                continue

            page_number = page.get("page")
            text = str(page.get("text", "")).strip()

            if not text:
                continue

            locator = f"page-{page_number}"

            evidence.append({
                **base,
                "evidence_id": make_evidence_id(record, locator),
                "locator": locator,
                "text": text,
            })

    # Excel: preserve sheet names and individual rows
    elif isinstance(content, dict):
        for sheet_name, rows in content.items():
            if not isinstance(rows, list):
                continue

            for row_number, row in enumerate(rows, start=1):
                if not isinstance(row, dict):
                    continue

                fields = []

                for key, value in row.items():
                    if value is not None and str(value).strip():
                        fields.append(f"{key}: {value}")

                if not fields:
                    continue

                text = "\n".join(fields)
                locator = f"sheet-{sheet_name}-row-{row_number}"

                evidence.append({
                    **base,
                    "evidence_id": make_evidence_id(record, locator),
                    "locator": locator,
                    "text": text,
                })

    return evidence


def build_evidence_store():
    """Normalize all processed documents into evidence records."""

    documents = load_processed_documents()
    evidence_store = []

    for document in documents:
        evidence_store.extend(normalize_document(document))

    return evidence_store


if __name__ == "__main__":
    evidence = build_evidence_store()

    print("DOCUMENTS LOADED:", len(load_processed_documents()))
    print("EVIDENCE RECORDS:", len(evidence))

    for item in evidence[:5]:
        print("\nID:", item["evidence_id"])
        print("SOURCE:", item["source_file"])
        print("LOCATION:", item["locator"])
        print("PREVIEW:", item["text"][:200])
