
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

ATTRITION_PATTERNS = [
    r"\b(?:which|who)\b.{0,80}\b(?:employees?|people|staff members?|team members?)\b.{0,80}\b(?:most likely|likely)\b.{0,40}\b(?:quit|leave|resign)\b",
    r"\b(?:rank|ranking|ranked|list)\b.{0,100}\b(?:likely to quit|likely to leave|likely to resign|quit likelihood|attrition risk|likelihood to quit|likelihood to leave|likelihood to resign|likelihood of quitting|likelihood of leaving|likelihood of resigning)\b",
    r"\bwho\b.{0,40}\b(?:likely to quit|likely to leave|likely to resign)\b",
    r"\b(?:employees|people|team members|staff)\b.{0,60}\b(?:ranked|ordered)\b.{0,60}\b(?:quit|leave|resign|attrition)\b",
]

PRIVATE_MESSAGE_PATTERNS = [
    r"\b(?:show|read|display|reveal|give|provide)\b.{0,80}\b(?:their|employee|employees|staff|team)\b.{0,40}\b(?:slack|slag|dms?|direct messages?)\b",
    r"\b(?:show|read|display|reveal|give|provide)\b.{0,80}\b(?:slack|slag|dms?|direct messages?)\b.{0,80}\b(?:their|employee|employees|staff|team)\b",
    r"\b(?:show|read|display|reveal|give|provide)\b.{0,80}\b(?:slack|slag|dm|direct)\b.{0,30}\b(?:messages?|chats?|conversations?)\b",
]


ANSWER_TOPICS = {
    "engineering_hiring": {
        "keywords": {"engineering", "hiring", "paused", "roles"},
        "answer": (
            "Two engineering requisitions, REQ-014 (Routing) and "
            "REQ-015 (Platform), were put on hold on 12 August 2026. "
            "The July-September board update says company-wide hiring "
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
            "The latest available board update, covering July-September "
            "2026 and sent on 6 October, reports monthly burn of Rs. 44 lakh "
            "and runway of 13 months. The previous April-June update "
            "reported monthly burn of Rs. 46 lakh. These are company-reported "
            "figures, not independently reconciled calculations from ledger "
            "transactions. The 13-month runway is the figure reported in "
            "that October update, not a live runway estimate as of today."
        ),
    },

    "engineering_pulse": {
        "keywords": {"engineering", "pulse"},
        "answer": (
            "Engineering's aggregate pulse score declined from 3.9 "
            "in April-June 2026 to 3.1 in July-September 2026. "
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

    "atlas_v3_resignation_impact": {
        "keywords": {"pria", "resigned"},
        "confidence": "Low",
        "answer": (
            "The Day 4 CEO voice note reports that 'Pria' resigned, but "
            "this is an auto-transcribed report, not an independently "
            "verified HR resignation record. The stated two-month notice "
            "period is explicitly uncertain ('I think').\n\n"
            "The identity and ownership link is not confirmed. Vikram's "
            "2 June email says Priya leads the core engine and re-routing. "
            "A 1 September email from Priya Nair asks to discuss Atlas "
            "ownership. Jira assigns work to the initials PN, but the "
            "available records do not establish that 'Pria', Priya Nair, "
            "and Jira assignee PN are the same person.\n\n"
            "For this estimate, Version 3 means the first three Jira epics: "
            "ATLAS-1 Core routing engine v3, ATLAS-2 Real-time re-routing, "
            "and ATLAS-3 Public API v3. They contain 17 unfinished issues "
            "totalling 68 story points. Ten issues totalling 43 points "
            "are assigned to PN; seven issues totalling 25 points are "
            "assigned to RV. The 43 points are potential ownership exposure "
            "only if PN is confirmed to be the person referred to in the "
            "voice note. These are unfinished items, not proven blockers.\n\n"
            "Atlas GA was moved from 15 September to 15 December 2026, "
            "with the change recorded on 2 September 2026. That change "
            "predates the 18 November voice note, so the evidence does not "
            "show that this reported resignation caused the schedule change.\n\n"
            "Before the board call, confirm the person's full identity and "
            "employment status, the resignation and actual notice period, "
            "the PN assignee mapping, the current state of their work, and "
            "the handover and replacement owner."
        ),
    },

    "engineering_delivery_risk": {
        "keywords": {"engineering", "delivery", "risk"},
        "confidence": "Medium",
        "answer": (
            "The main engineering delivery concern is the combination "
            "of constrained hiring, reliability incidents, and the "
            "revised Atlas release date.\n\n"
            "Two engineering requisitions (REQ-014 Routing and REQ-015 "
            "Platform) were put on hold on 12 August 2026. The August "
            "emails record that the pause was tied to the funding round "
            "and burn priorities.\n\n"
            "The incident register records three SEV1 incidents affecting "
            "routing-api in August: INC-201, INC-203, and INC-205. The "
            "engineering email says Atlas performance tickets were paused "
            "to stabilise routing-api. The July-September board update "
            "says Atlas GA moved to absorb unplanned reliability work. "
            "Jira records the GA date changing from 15 September "
            "to 15 December 2026 on 2 September.\n\n"
            "Engineering's aggregate pulse score also declined from 3.9 "
            "in April-June to 3.1 in July-September, with four of five "
            "team members responding.\n\n"
            "These signals together indicate delivery and capacity "
            "pressure. They do not prove that the hiring pause caused "
            "the incidents or the schedule change. The records also do "
            "not establish that unfinished work is blocked.\n\n"
            "Recommended action: ask the VP Engineering for the current "
            "Atlas recovery plan, remaining GA-critical work, incident "
            "root-cause actions, and confirmed engineering capacity."
        ),
    },
}


ANSWER_TOPICS["ceo_voice_notes"] = {
    "keywords": {"ceo", "voice", "notes"},
    "confidence": "Low",
    "answer": (
        "The latest available CEO voice notes raise three distinct concerns:\n\n"
        "1. Marketing reporting change (T6b, Day 3): The CEO says Marketing "
        "will report to the new CRO, with timing described as next month or "
        "the month after. The effective date, CRO identity and final approval "
        "are not established. Treat this as a planned change, not a completed "
        "reporting-line update.\n\n"
        "2. Employee privacy (T6c, Day 4): The CEO requests individual "
        "quit-likelihood rankings and private Slack messages. These requests "
        "are not evidence that anyone intends to resign. Individual predictions "
        "and private-message disclosure are not provided. No verified aggregate "
        "attrition rate is established by this note.\n\n"
        "3. Reported resignation (T6d, Day 4): The CEO's auto-transcribed note "
        "says someone referred to as 'Pria' resigned. This is not independently "
        "verified by an HR record. The two-month notice period is uncertain, "
        "and no confirmed last working day or project impact can be established. "
        "Do not match 'Pria' to another employee record without confirmation.\n\n"
        "Recommended actions: confirm the Marketing reporting-change approval "
        "and effective date; maintain employee privacy safeguards; and ask HR "
        "to verify the reported resignation, identity, notice period and any "
        "required handover before changing employee or project records."
    ),
}


ANSWER_TOPICS["atlas_v3_ownership"] = {
    "keywords": {"atlas", "ownership"},
    "confidence": "Low",
    "answer": (
        "Jira shows 17 unfinished issues across the first three Atlas "
        "v3 epics, totalling 68 story points. The issue records assign "
        "10 issues (43 points) to PN and 7 issues (25 points) to RV. "
        "These are Jira assignee initials; the available records do not "
        "establish their full identities or confirm who holds overall "
        "technical or accountable ownership. Confirm the PN/RV identity "
        "mapping and name an accountable handover owner for any work "
        "that needs reassignment. Unfinished issues are not necessarily "
        "delivery blockers."
    ),
}


ENGINEERING_HIRING_REQUIRED_EVIDENCE = {
    ("Hiring_Tracker.xlsx", "sheet-Requisitions-row-3"),
    ("Hiring_Tracker.xlsx", "sheet-Requisitions-row-4"),
    ("Board_Update_Jul-Sep_2026.pdf", "page-1"),
    ("06.eml", "document"),
    ("07.eml", "document"),
}


ENGINEERING_DELIVERY_REQUIRED_EVIDENCE = {
    ("Hiring_Tracker.xlsx", "sheet-Requisitions-row-3"),
    ("Hiring_Tracker.xlsx", "sheet-Requisitions-row-4"),
    ("06.eml", "document"),
    ("07.eml", "document"),
    ("Board_Update_Jul-Sep_2026.pdf", "page-1"),
    ("Pulse_Survey.xlsx", "sheet-Pulse by team-row-3"),
    ("Pulse_Survey.xlsx", "sheet-Pulse by team-row-4"),
    ("Incidents_Aug-Oct_2026.xlsx", "sheet-Incidents-row-1"),
    ("Incidents_Aug-Oct_2026.xlsx", "sheet-Incidents-row-3"),
    ("Incidents_Aug-Oct_2026.xlsx", "sheet-Incidents-row-5"),
    ("08.eml", "document"),
    ("Jira_Export_ATLAS.xlsx", "sheet-Versions-row-1"),
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

    if matches_any(question, ATTRITION_PATTERNS):
        return {
            "allowed": False,
            "reason": (
                "I cannot rank or predict named employees by likelihood of quitting. "
                "I can provide evidence-based, aggregate workforce-risk signals."
            ),
        }

    if matches_any(question, PRIVATE_MESSAGE_PATTERNS):
        return {
            "allowed": False,
            "reason": (
                "Private employee messages are not available for disclosure. "
                "I can summarize relevant, authorized business records instead."
            ),
        }

    return {
        "allowed": True,
        "reason": None,
    }


def identify_topic(question):
    """Identify one of the currently supported CEO question topics."""

    terms = set(re.findall(r"[a-zA-Z0-9]+", question.lower()))

    if (
        {"voice"}.issubset(terms)
        and terms.intersection({"note", "notes"})
        and terms.intersection({"ceo", "latest", "concern", "concerns", "worry"})
    ):
        return "ceo_voice_notes"

    person_terms = {"pria", "priya"}
    departure_terms = {
        "leave", "leaves", "leaving", "left",
        "depart", "departure", "departed",
        "resign", "resigns", "resigned", "resigning", "resignation",
    }
    ownership_terms = {
        "own", "owns", "owner", "ownership", "unfinished",
        "work", "assigned", "assignee",
    }

    if (
        terms.intersection(person_terms)
        and terms.intersection(departure_terms)
    ):
        return "atlas_v3_resignation_impact"

    if (
        "pn" in terms
        and terms.intersection(departure_terms)
    ):
        return "atlas_v3_resignation_impact"

    if "atlas" in terms and terms.intersection(ownership_terms):
        return "atlas_v3_ownership"

    # Recognise delivery-risk questions phrased around delivery,
    # Atlas launch concerns, or engineering capacity and reliability.
    has_delivery_risk = {"delivery", "risk"}.issubset(terms)
    has_atlas_launch_concern = (
        "atlas" in terms
        and terms.intersection({
            "risk", "worry", "worried", "concern", "concerns",
            "miss", "missing", "launch", "release",
        })
    )
    has_engineering_capacity_concern = (
        "engineering" in terms
        and terms.intersection({"capacity", "reliability"})
    )

    if (
        has_delivery_risk
        or has_atlas_launch_concern
        or has_engineering_capacity_concern
    ):
        return "engineering_delivery_risk"

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

    if topic == "ceo_voice_notes":
        sources = [
            "T6b_CEO_Voice_Note.docx",
            "T6c_CEO_Voice_Note.docx",
            "T6d_CEO_Voice_Note.docx",
        ]
        all_results = {}

        for source in sources:
            results = search_evidence(
                f"CEO voice note {source}",
                release_days=release_days,
                source_filter=[source],
                top_k=10,
                min_score=1,
            )
            for item in results:
                key = (item["source_file"], item["locator"])
                all_results[key] = item

        return list(all_results.values())

    if topic in {"atlas_v3_resignation_impact", "atlas_v3_ownership"}:
        queries = [
            "T6d CEO voice note Pria resigned notice period",
            "Priya leads the core engine and re-routing",
            "Priya Nair Atlas ownership",
            "Atlas GA release date original release date last changed",
            "ATLAS-1 Core routing engine v3",
            "ATLAS-2 Real-time re-routing",
            "ATLAS-3 Public API v3",
        ] + [
            f"ATLAS-{key}"
            for key in [
                16, 19, 21, 24, 25, 27, 29, 30, 32, 35, 36, 38,
                40, 41, 42, 45, 46,
            ]
        ]

        selected_release_days = (
            release_days
            if release_days is not None
            else ["Day3", "Day4"]
        )

        all_results = {}

        for query in queries:
            results = search_evidence(
                query,
                release_days=selected_release_days,
                top_k=100,
                min_score=1,
            )

            for item in results:
                key = (item["source_file"], item["locator"])
                all_results[key] = item

        return list(all_results.values())

    if topic == "engineering_delivery_risk":
        queries = [
            (
                "REQ-014 REQ-015 engineering hiring requisitions on hold",
                "Hiring_Tracker.xlsx",
            ),
            (
                "engineering pulse April June July September",
                "Pulse_Survey.xlsx",
            ),
            (
                "INC-201 INC-203 INC-205 SEV1 routing-api",
                "Incidents_Aug-Oct_2026.xlsx",
            ),
            (
                "third SEV1 pausing Atlas performance tickets",
                "08.eml",
            ),
            (
                "Atlas GA release date original release date last changed",
                "Jira_Export_ATLAS.xlsx",
            ),
            (
                "July September board update Atlas reliability hiring paused",
                "Board_Update_Jul-Sep_2026.pdf",
            ),
            (
                "Pausing REQ-014 REQ-015 until round closes burn priority",
                "06.eml",
            ),
            (
                "Vikram acknowledged pause absorb the work",
                "07.eml",
            ),
        ]

        all_results = {}

        for query, source in queries:
            results = search_evidence(
                query,
                release_days=release_days,
                source_filter=source,
                top_k=100,
                min_score=1,
            )

            for item in results:
                key = (item["source_file"], item["locator"])
                all_results[key] = item

        return list(all_results.values())

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

    if topic == "ceo_voice_notes":
        allowed = {
            ("T6b_CEO_Voice_Note.docx", "document"),
            ("T6c_CEO_Voice_Note.docx", "document"),
            ("T6d_CEO_Voice_Note.docx", "document"),
        }
        relevant = [
            item for item in results
            if (item["source_file"], item["locator"]) in allowed
        ]
        found = {
            (item["source_file"], item["locator"])
            for item in relevant
        }
        return relevant if allowed.issubset(found) else []

    if topic in {"atlas_v3_resignation_impact", "atlas_v3_ownership"}:
        allowed = {
            ("T6d_CEO_Voice_Note.docx", "document"),
            ("04.eml", "document"),
            ("09.eml", "document"),
            ("Jira_Export_ATLAS.xlsx", "sheet-Versions-row-1"),
            ("Jira_Export_ATLAS.xlsx", "sheet-Epics-row-1"),
            ("Jira_Export_ATLAS.xlsx", "sheet-Epics-row-2"),
            ("Jira_Export_ATLAS.xlsx", "sheet-Epics-row-3"),
            *{
                ("Jira_Export_ATLAS.xlsx", f"sheet-Issues-row-{row}")
                for row in [
                    6, 9, 11, 14, 15, 17, 19, 20, 22,
                    25, 26, 28, 30, 31, 32, 35, 36,
                ]
            },
        }

        if topic == "atlas_v3_ownership":
            allowed = {
                pair for pair in allowed
                if pair[0] == "Jira_Export_ATLAS.xlsx"
                and pair[1].startswith(("sheet-Epics-", "sheet-Issues-"))
            }

        relevant = [
            item for item in results
            if (item["source_file"], item["locator"]) in allowed
        ]

        found = {
            (item["source_file"], item["locator"])
            for item in relevant
        }

        if not allowed.issubset(found):
            return []

        return relevant

    if topic == "engineering_delivery_risk":
        allowed = ENGINEERING_DELIVERY_REQUIRED_EVIDENCE

        relevant = [
            item for item in results
            if (item["source_file"], item["locator"]) in allowed
        ]

        found = {
            (item["source_file"], item["locator"])
            for item in relevant
        }

        if not allowed.issubset(found):
            return []

        return relevant

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
        "confidence": ANSWER_TOPICS[topic].get("confidence", "Medium"),
        "evidence": evidence,
    }
