
import re
import sys
from pathlib import Path

BACKEND_APP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_APP))

from rag.evidence_store import build_evidence_store


STOP_WORDS = {
    "the", "is", "are", "was", "were", "a", "an", "and",
    "or", "of", "to", "in", "on", "for", "from", "with",
    "what", "when", "where", "who", "how", "much", "many",
    "did", "does", "do", "has", "have", "had", "tell", "me",
    "about", "show", "give", "please", "company", "veloxa",
    "why", "happened", "happen", "reason", "latest",
    "current", "recent", "score", "their", "they", "it",
    "were", "was", "been", "being"
}

# Expand common terms without changing the original query.
SYNONYMS = {
    "resign": {"resignation", "resigned", "exit", "departure"},
    "resigned": {"resignation", "resign", "exit", "departure"},
    "resignation": {"resign", "resigned", "exit", "departure"},
    "pulse": {"engagement", "survey"},
    "engagement": {"pulse", "survey"},
    "hiring": {"requisition", "requisitions", "recruitment"},
    "paused": {"pause", "hold", "on"},
    "pause": {"paused", "hold"},
    "burn": {"spending", "expense", "expenses"},
}

# These files are useful for project context, but not primary
# evidence for answering factual CEO questions.
EXCLUDED_FILES = {
    "README.txt",
    "Evidence_Index.xlsx",
    "Entity_Resolution.xlsx",
    "Connection_Worksheet.pdf",
    "Candidate_Brief.docx",
    "Payroll_Register_Jan-Mar_2026.xlsx",
}


def tokenize(text):
    """Convert text into lowercase searchable terms."""

    words = re.findall(r"[a-zA-Z0-9]+", text.lower())

    return {
        word for word in words
        if word not in STOP_WORDS and len(word) > 1
    }


def expand_query_terms(query_terms):
    """Add useful synonyms to the query."""

    expanded = set(query_terms)

    for term in query_terms:
        expanded.update(SYNONYMS.get(term, set()))

    return expanded


def get_source_weight(source_file):
    """Prefer original records over machine-generated summaries."""

    name = source_file.lower()

    if name.endswith(".docx") and "call" in name:
        return 0.75

    if name.endswith(".pdf") and "board_update" in name:
        return 1.3

    if name.endswith(".pdf") and "resignation" in name:
        return 1.5

    if name.endswith(".eml"):
        return 1.4

    if name.endswith(".xlsx"):
        return 1.3

    return 1.0



def get_recency_bonus(item, query):
    """Prefer newer board updates when latest data is requested."""

    query_lower = query.lower()

    if "latest" not in query_lower and "recent" not in query_lower:
        return 0

    source = item["source_file"].lower()

    if "jul-sep_2026" in source:
        return 3

    if "apr-jun_2026" in source:
        return 1

    return 0



def search_evidence(
    query,
    release_days=None,
    top_k=5,
    min_score=1
):
    """
    Retrieve evidence using weighted keyword matching.

    This is a keyword-based retrieval system, not a semantic RAG model.
    Release-day filtering does not replace event-date filtering.
    """

    if not isinstance(query, str) or not query.strip():
        return []

    if top_k < 1:
        return []

    query_terms = tokenize(query)

    if not query_terms:
        return []

    expanded_terms = expand_query_terms(query_terms)

    evidence_store = build_evidence_store()
    results = []

    for item in evidence_store:

        if (
            release_days is not None
            and item["release_day"] not in release_days
        ):
            continue

        if item["source_file"] in EXCLUDED_FILES:
            continue

        document_terms = tokenize(item["text"])

        matched_terms = expanded_terms.intersection(document_terms)

        if not matched_terms:
            continue

        # Original query matches are more valuable than synonyms.
        exact_matches = query_terms.intersection(document_terms)

        score = (
            len(exact_matches) * 2
            + len(matched_terms - exact_matches)
        )

        source_weight = get_source_weight(item["source_file"])
        recency_bonus = get_recency_bonus(item, query)

        final_score = score * source_weight + recency_bonus

        if final_score < min_score:
            continue

        results.append({
            **item,
            "score": round(final_score, 2),
            "matched_terms": sorted(matched_terms),
            "citation": (
                f'{item["source_file"]} '
                f'({item["locator"]}, {item["release_day"]})'
            )
        })

    results.sort(
        key=lambda item: (
            -item["score"],
            item["source_file"],
            item["locator"]
        )
    )

    return results[:top_k]


if __name__ == "__main__":

    questions = [
        "What is the latest monthly burn?",
        "Why were engineering hiring roles paused?",
        "What happened to the engineering pulse score?",
        "Why did Siddharth resign?"
    ]

    for question in questions:

        print("\n" + "=" * 65)
        print("QUESTION:", question)

        results = search_evidence(
            question,
            release_days=["Day1", "Day2"],
            top_k=5
        )

        if not results:
            print("NO MATCHING EVIDENCE")
            continue

        for result in results:

            print("\nSCORE:", result["score"])
            print("CITATION:", result["citation"])
            print("MATCHED TERMS:", result["matched_terms"])
            print("EVIDENCE:", result["text"][:500])
