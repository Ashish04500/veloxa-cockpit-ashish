
import sys
from pathlib import Path

BACKEND_APP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_APP))

from rag.retriever import search_evidence


def collect_evidence(
    query,
    allowed_sources,
    required_terms=None,
    top_k=30,
    release_days=None
):
    """Retrieve and filter evidence using source and content constraints."""

    results = search_evidence(
        query,
        release_days=(
            release_days
            if release_days is not None
            else ["Day1", "Day2", "Day3"]
        ),
        top_k=top_k
    )

    selected = []
    required_terms = required_terms or []

    for item in results:
        source = item["source_file"].lower()
        content = item["text"].lower()

        source_allowed = any(
            name.lower() in source
            for name in allowed_sources
        )

        terms_match = all(
            term.lower() in content
            for term in required_terms
        )

        if source_allowed and terms_match:
            selected.append({
                "source": item["source_file"],
                "citation": item["citation"],
                "evidence": item["text"][:500]
            })

    return selected


def build_risk(
    risk_id,
    title,
    confidence,
    impact,
    urgency,
    explanation,
    action,
    evidence,
    uncertainty
):
    """Create a risk record with a transparent prioritisation score."""

    impact_points = {
        "High": 3,
        "Medium": 2,
        "Low": 1
    }

    unique_sources = {
        item["source"] for item in evidence
    }

    evidence_strength = min(len(unique_sources), 3)

    score = (
        impact_points[impact] * 3
        + urgency * 2
        + evidence_strength
    )

    return {
        "risk_id": risk_id,
        "title": title,
        "priority": None,
        "confidence": confidence,
        "impact": impact,
        "urgency": urgency,
        "evidence_strength": evidence_strength,
        "score": score,
        "explanation": explanation,
        "recommended_action": action,
        "evidence": evidence,
        "uncertainty": uncertainty
    }


def get_top_risks():
    """Build and rank the current provisional top-three CEO risks."""

    engineering_evidence = (
        collect_evidence(
            "engineering hiring roles paused",
            ["Hiring_Tracker.xlsx"],
            ["REQ-014"]
        )
        + collect_evidence(
            "engineering hiring roles paused",
            ["Hiring_Tracker.xlsx"],
            ["REQ-015"]
        )
        + collect_evidence(
            "engineering pulse score",
            ["Pulse_Survey.xlsx"],
            ["Team: Engineering", "Quarter: Jul-Sep 2026"]
        )
        + collect_evidence(
            "engineering pulse score",
            ["Pulse_Survey.xlsx"],
            ["Team: Engineering", "Quarter: Apr-Jun 2026"]
        )
        + collect_evidence(
            "Atlas reliability work delay",
            ["Board_Update_Jul-Sep_2026.pdf"]
        )
        + collect_evidence(
            "Atlas GA release date original release date",
            ["Jira_Export_ATLAS.xlsx"],
            [
                "Original Release Date: 2026-09-15",
                "Release Date: 2026-12-15"
            ]
        )
        + collect_evidence(
            "INC-201 SEV1 routing-api",
            ["Incidents_Aug-Oct_2026.xlsx"],
            ["INC-201", "SEV1", "routing-api"]
        )
        + collect_evidence(
            "INC-203 SEV1 routing-api",
            ["Incidents_Aug-Oct_2026.xlsx"],
            ["INC-203", "SEV1", "routing-api"]
        )
        + collect_evidence(
            "INC-205 SEV1 routing-api",
            ["Incidents_Aug-Oct_2026.xlsx"],
            ["INC-205", "SEV1", "routing-api"]
        )
    )

    marketing_evidence = (
        collect_evidence(
            "Siddharth resignation",
            ["Resignation_Letter_SM.pdf"]
        )
        + collect_evidence(
            "Product Marketing Manager backfill open",
            ["Hiring_Tracker.xlsx"],
            ["REQ-016"]
        )
    )

    runway_evidence = (
        collect_evidence(
            "latest monthly burn runway",
            [
                "Board_Update_Jul-Sep_2026.pdf",
                "Board_Update_Apr-Jun_2026.pdf"
            ]
        )
        + collect_evidence(
            "hiring paused until funding round",
            ["06.eml"]
        )
    )

    risks = [
        build_risk(
            risk_id="RISK-001",
            title="Atlas delivery and reliability risk",
            confidence="Medium-High",
            impact="High",
            urgency=5,
            explanation=(
                "The Atlas GA release date was revised from "
                "15 September to 15 December 2026 on 2 September "
                "by Vikram. The incident register records three August "
                "SEV1 incidents affecting routing-api, all assigned "
                "to Sneha. Earlier evidence also shows two engineering "
                "requisitions were paused and the engineering pulse "
                "score declined to 3.1. Together, these indicate "
                "delivery and reliability pressure."
            ),
            action=(
                "Ask the VP Engineering for an updated Atlas recovery "
                "plan, the remaining GA-critical work, incident "
                "root-cause actions, and current engineering capacity."
            ),
            evidence=engineering_evidence,
            uncertainty=(
                "The Jira export does not establish that every "
                "unresolved ticket blocks GA. The incident records "
                "establish severity and responders but do not establish "
                "root causes. The evidence does not prove that the "
                "hiring pause caused the schedule revision or "
                "reliability incidents."
            )
        ),

        build_risk(
            risk_id="RISK-002",
            title="Marketing continuity and knowledge-transfer risk",
            confidence="Medium",
            impact="Medium",
            urgency=4,
            explanation=(
                "The Product Marketing Manager submitted a resignation "
                "with a last working day of 31 October 2026. A Product "
                "Marketing Manager backfill requisition is open."
            ),
            action=(
                "Confirm launch-kit handover, assign ownership of "
                "active launches, and review the backfill plan."
            ),
            evidence=marketing_evidence,
            uncertainty=(
                "The resignation is confirmed, but actual handover "
                "completion or disruption to launches has not been established."
            )
        ),

        build_risk(
            risk_id="RISK-003",
            title="Funding and runway watch",
            confidence="Medium",
            impact="High",
            urgency=3,
            explanation=(
                "The latest board update reports 13 months of runway, "
                "down from 14 months in the previous update. Monthly "
                "burn declined from Rs. 46L to Rs. 44L. Hiring pauses were "
                "linked to the funding round."
            ),
            action=(
                "Ask Finance for an updated cash forecast, funding "
                "round status, and runway sensitivity under different "
                "funding scenarios."
            ),
            evidence=runway_evidence,
            uncertainty=(
                "The available records do not establish that the "
                "funding round has failed or that cash is immediately "
                "at risk. Burn has also declined."
            )
        )
    ]

    # Rank risks by calculated score, highest first.
    ranked_risks = sorted(
        risks,
        key=lambda risk: risk["score"],
        reverse=True
    )

    # Assign display priorities after ranking.
    for index, risk in enumerate(ranked_risks, start=1):
        risk["priority"] = index

    return ranked_risks


if __name__ == "__main__":
    risks = get_top_risks()

    print("\nVELOXA CEO RISK SUMMARY")
    print("=" * 60)

    for risk in risks:
        print(f"\nPRIORITY {risk['priority']}: {risk['title']}")
        print("RISK SCORE:", risk["score"], "/ 22")
        print("CONFIDENCE:", risk["confidence"])
        print("IMPACT:", risk["impact"])
        print("URGENCY:", risk["urgency"], "/ 5")
        print(
            "EVIDENCE STRENGTH:",
            risk["evidence_strength"],
            "/ 3"
        )
        print("EXPLANATION:", risk["explanation"])
        print("RECOMMENDED ACTION:", risk["recommended_action"])
        print("UNCERTAINTY:", risk["uncertainty"])

        print("EVIDENCE:")

        if not risk["evidence"]:
            print("NO MATCHING EVIDENCE FOUND")
        else:
            for evidence in risk["evidence"]:
                print("-", evidence["citation"])
                print(" ", evidence["evidence"][:250])

        print("-" * 60)
