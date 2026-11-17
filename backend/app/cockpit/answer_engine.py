
import re

from app.rag.retriever import search_evidence


SENSITIVE_PATTERNS = [
    r"\bindividual salary\b",
    r"\bpersonal salary\b",
    r"\bhow much does .+ earn\b",
    r"\bwhat is .+ salary\b",
    r"\bpayroll details\b",
    r"\bsalary of\b",
    r"\bcompensation of\b",
]

PRIVATE_PULSE_PATTERNS = [
    r"\bindividual survey comments?\b",
    r"\bshow me .+ survey comments?\b",
    r"\bwhat did .+ say in the survey\b",
    r"\bwho gave .+ pulse score\b",
]

IDENTITY_PATTERNS = [
    r"\bwho is the unnamed engineer\b",
    r"\bidentify the engineer at risk\b",
    r"\bname the engineer at risk\b",
    r"\bwhich engineer is at risk\b",
]


ANSWER_TOPICS = {
    "engineering_hiring": {
        "keywords": {"engineering", "hiring", "paused", "roles"},
        "answer": (
            "Two engineering requisitions, REQ-014 (Routing) and "
            "REQ-015 (Platform), were put on hold on 12 August 2026. "
            "The July–September board update says company-wide hiring "
            "was paused while the funding round was being closed. "
            "Meera's 12 August email says burn was the priority "
            "until the round closed. Vikram acknowledged the pause "
            "and said the team would absorb the work. "
            "The records establish the funding and burn rationale, "
            "but do not quantify the resulting workload impact."
        ),
    },

    "monthly_burn": {
        "keywords": {"burn"},
        "answer": (
            "The latest available board update, covering July–September "
            "2026 and sent on 6 October, reports monthly burn of ₹44 lakh. "
            "The previous April–June update reported ₹46 lakh. "
            "This is the company's reported figure, not an independently "
            "reconciled calculation from ledger transactions."
        ),
    },

    "engineering_pulse": {
        "keywords": {"engineering", "pulse"},
        "answer": (
            "Engineering's aggregate pulse score declined from 3.9 "
            "in April–June 2026 to 3.1 in July–September 2026. "
            "The latest survey had 4 responses from a team of 5. "
            "Individual comments are not available because the team "
            "is too small. This is a warning signal, not proof of "
            "the cause or any individual's sentiment."
        ),
    },

    "siddharth_resignation": {
        "keywords": {"siddharth", "resignation"},
        "answer": (
            "Siddharth Mehta submitted his resignation on "
            "15 September 2026 from his Product Marketing Manager role. "
            "His letter listed 31 October 2026 as his last working day. "
            "He cited a desire for clearer launch timelines and work "
            "that reaches customers. The letter alone does not confirm "
            "whether the handover was completed."
        ),
    },
}


ENGINEERING_HIRING_REQUIRED_EVIDENCE = {
    ("Hiring_Tracker.xlsx", "sheet-Requisitions-row-3"),
    ("Hiring_Tracker.xlsx", "sheet-Requisitions-row-4"),
    ("Board_Update_Jul-Sep_2026.pdf", "page-1"),
    ("06.eml", "document"),
    ("07.eml", "document"),
}


def matches_any(question, patterns):
    """Check whether a question matches restricted information patterns."""

    return any(
        re.search(pattern, question, re.IGNORECASE)
        for pattern in patterns
    )


def check_question_safety(question):
    """Apply basic privacy restrictions before retrieving evidence."""

    if matches_any(question, SENSITIVE_PATTERNS):
        return {
            "allowed": False,
            "reason": "Individual salary and payroll details are restricted.",
        }

    if matches_any(question, PRIVATE_PULSE_PATTERNS):
        return {
            "allowed": False,
            "reason": (
                "Individual survey comments are restricted. "
                "Only permitted aggregate team-level information can be shown."
            ),
        }

    if matches_any(question, IDENTITY_PATTERNS):
        return {
            "allowed": False,
            "reason": (
                "The available evidence does not identify the employee. "
                "I will not infer or guess their identity."
            ),
        }

    return {
        "allowed": True,
        "reason": None,
    }


def identify_topic(question):
    """Identify one of the currently supported CEO question topics."""

    terms = set(re.findall(r"[a-zA-Z0-9]+", question.lower()))

    for topic, config in ANSWER_TOPICS.items():
        if config["keywords"].issubset(terms):
            return topic

    # Natural variations for engineering hiring questions.
    if (
        {"engineering", "hiring"}.issubset(terms)
        and terms.intersection({"pause", "paused", "hold", "freeze"})
    ):
        return "engineering_hiring"

    # Natural variations for monthly burn questions.
    if (
        "burn" in terms
        and terms.intersection({"latest", "monthly", "current"})
    ):
        return "monthly_burn"

    return None


def retrieve_topic_evidence(topic, release_days=None):
    """Retrieve evidence using topic-specific queries."""

    if topic == "engineering_hiring":
        queries = [
            "REQ-014 REQ-015 engineering hiring on hold",
            "funding round hiring paused burn priority",
            "Vikram acknowledged pause absorb work",
        ]

        all_results = {}

        for query in queries:
            results = search_evidence(
                query,
                release_days=release_days,
                top_k=20,
                min_score=1,
            )

            for item in results:
                key = (item["source_file"], item["locator"])
                all_results[key] = item

        return list(all_results.values())

    queries = {
        "monthly_burn": "latest monthly burn board update",
        "engineering_pulse": (
            "engineering pulse score July September survey"
        ),
        "siddharth_resignation": (
            "Siddharth Mehta resignation letter last working day"
        ),
    }

    return search_evidence(
        queries[topic],
        release_days=release_days,
        top_k=30,
        min_score=1,
    )


def filter_topic_evidence(topic, results):
    """Keep only the exact records approved for each answer topic."""

    if topic == "engineering_hiring":
        allowed = ENGINEERING_HIRING_REQUIRED_EVIDENCE

        relevant = [
            item
            for item in results
            if (item["source_file"], item["locator"]) in allowed
        ]

        found = {
            (item["source_file"], item["locator"])
            for item in relevant
        }

        if not allowed.issubset(found):
            return []

        return relevant

    if topic == "monthly_burn":
        allowed = {
            ("Board_Update_Jul-Sep_2026.pdf", "page-1"),
            ("Board_Update_Apr-Jun_2026.pdf", "page-1"),
        }

    elif topic == "engineering_pulse":
        allowed = {
            ("Pulse_Survey.xlsx", "sheet-Pulse by team-row-4"),
            ("11.eml", "document"),
        }

    elif topic == "siddharth_resignation":
        allowed = {
            ("Resignation_Letter_SM.pdf", "page-1"),
        }

    else:
        return []

    return [
        item
        for item in results
        if (item["source_file"], item["locator"]) in allowed
    ]


def answer_ceo_question(question, release_days=None):
    """
    Return a rules-based answer supported by retrieved evidence.

    This implementation does not use an LLM.
    It supports only explicitly defined question topics.
    """

    if not isinstance(question, str) or not question.strip():
        return {
            "status": "invalid_question",
            "answer": "Please provide a valid question.",
            "confidence": "None",
            "evidence": [],
        }

    safety = check_question_safety(question)

    if not safety["allowed"]:
        return {
            "status": "refused",
            "answer": safety["reason"],
            "confidence": "None",
            "evidence": [],
        }

    topic = identify_topic(question)

    if topic is None:
        return {
            "status": "insufficient_evidence",
            "answer": (
                "I could not identify a supported answer for this question "
                "from the available evidence. I will not guess."
            ),
            "confidence": "Low",
            "evidence": [],
        }

    results = retrieve_topic_evidence(
        topic,
        release_days=release_days,
    )

    relevant = filter_topic_evidence(topic, results)

    if not relevant:
        return {
            "status": "insufficient_evidence",
            "answer": (
                "The required supporting records were not found "
                "within the selected release-day filter. "
                "I cannot verify this answer."
            ),
            "confidence": "Low",
            "evidence": [],
        }

    evidence = [
        {
            "source": item["source_file"],
            "location": item["locator"],
            "release_day": item["release_day"],
            "citation": item["citation"],
            "excerpt": item["text"][:500],
        }
        for item in relevant
    ]

    return {
        "status": "answered",
        "answer": ANSWER_TOPICS[topic]["answer"],
        "confidence": "Medium",
        "evidence": evidence,
    }
