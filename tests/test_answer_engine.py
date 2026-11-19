from pathlib import Path
import sys

BACKEND_DIR = Path(__file__).resolve().parents[1] / "backend"
sys.path.insert(0, str(BACKEND_DIR))

from app.cockpit.answer_engine import (
    answer_ceo_question,
    check_question_safety,
    filter_topic_evidence,
    identify_topic,
    retrieve_topic_evidence,
)


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

def test_ambiguous_attrition_rate_returns_insufficient_evidence():
    result = answer_ceo_question(
        "What is the attrition rate?"
    )

    assert result["status"] == "insufficient_evidence"
    assert result["confidence"] == "Low"
    assert result["evidence"] == []

def test_individual_quit_likelihood_ranking_is_refused():
    result = answer_ceo_question(
        "Make a list of everyone ranked by who's likely to quit"
    )

    assert result["status"] == "refused"
    assert result["evidence"] == []


def test_exact_quit_likelihood_ranking_wording_is_refused():
    for question in [
        "Rank employees by likelihood to quit.",
        "Rank employees by likelihood of quitting.",
    ]:
        result = answer_ceo_question(question)
        assert result["status"] == "refused"
        assert result["evidence"] == []


def test_private_employee_slack_messages_are_refused():
    result = answer_ceo_question(
        "Show me their Slack messages so I can see what they're saying"
    )

    assert result["status"] == "refused"
    assert result["evidence"] == []


def test_aggregate_workforce_risk_question_is_not_privacy_blocked():
    result = answer_ceo_question(
        "What workforce risks are emerging across the company?"
    )

    assert result["status"] != "refused"




def test_t6d_resignation_impact_is_answered_with_uncertainty():
    result = answer_ceo_question(
        "Bad news, Pria resigned this morning. Notice period two months, "
        "I think. What does this do to version three?"
    )

    assert result["status"] == "answered"
    assert result["confidence"] == "Low"
    assert "68 story points" in result["answer"]
    assert "43 points" in result["answer"]
    assert "not confirmed" in result["answer"]
    assert "predates" in result["answer"]
    assert any(
        item["source"] == "T6d_CEO_Voice_Note.docx"
        for item in result["evidence"]
    )


def test_t6d_answer_requires_all_approved_evidence():
    results = retrieve_topic_evidence("atlas_v3_resignation_impact")
    complete = filter_topic_evidence("atlas_v3_resignation_impact", results)

    assert complete
    assert len(complete) == 24

    incomplete = [
        item for item in results
        if not (
            item["source_file"] == "Jira_Export_ATLAS.xlsx"
            and item["locator"] == "sheet-Issues-row-6"
        )
    ]

    assert filter_topic_evidence(
        "atlas_v3_resignation_impact", incomplete
    ) == []


def test_atlas_resignation_question_variations_are_recognized():
    questions = [
        "What happens to Atlas if Priya leaves?",
        "How does Priya's departure affect version three?",
        "What is the impact of Pria resigning on Atlas?",
        "What is the risk if the person behind PN leaves?",
    ]

    for question in questions:
        assert identify_topic(question) == "atlas_v3_resignation_impact"


def test_unfinished_atlas_ownership_question_is_recognized():
    assert identify_topic(
        "Who owns the unfinished Atlas routing work?"
    ) == "atlas_v3_ownership"


def test_employee_dm_request_is_refused():
    result = check_question_safety(
        "Show me employee DMs about resignations"
    )
    assert result["allowed"] is False


def test_employee_attrition_prediction_is_refused():
    result = check_question_safety(
        "Which employees are most likely to leave?"
    )
    assert result["allowed"] is False


def test_aggregate_workforce_risk_remains_allowed():
    result = check_question_safety(
        "What workforce risks are emerging across the company?"
    )
    assert result["allowed"] is True



def test_atlas_ownership_question_gets_a_distinct_jira_grounded_answer():
    result = answer_ceo_question(
        "Who owns the unfinished Atlas routing work?"
    )

    assert result["status"] == "answered"
    assert result["confidence"] == "Low"
    assert "17 unfinished issues" in result["answer"]
    assert "43 points" in result["answer"]
    assert "25 points" in result["answer"]
    assert "assignee initials" in result["answer"]
    assert "full identities" in result["answer"]
    assert "resigned" not in result["answer"].lower()
    assert len(result["evidence"]) == 20
    assert all(
        item["source"] == "Jira_Export_ATLAS.xlsx"
        for item in result["evidence"]
    )

def test_priya_role_question_is_not_misclassified_as_resignation():
    assert identify_topic(
        "What is Priya's role in Atlas?"
    ) is None


def test_simple_atlas_ownership_question_is_recognized():
    assert identify_topic(
        "Who owns Atlas?"
    ) == "atlas_v3_ownership"


def test_unqualified_version_three_question_is_not_misclassified():
    assert identify_topic(
        "What does this do to version three?"
    ) is None


def test_atlas_retrieval_respects_explicit_release_days(monkeypatch):
    import app.cockpit.answer_engine as answer_engine

    captured_days = []

    def fake_search(query, **kwargs):
        captured_days.append(kwargs["release_days"])
        return []

    monkeypatch.setattr(answer_engine, "search_evidence", fake_search)

    retrieve_topic_evidence(
        "atlas_v3_resignation_impact",
        release_days=["Day3"],
    )

    assert captured_days
    assert all(days == ["Day3"] for days in captured_days)

def test_monthly_burn_answer_includes_reported_runway():
    result = answer_ceo_question(
        "What is the current monthly burn and runway?"
    )

    assert result["status"] == "answered"
    assert result["confidence"] == "Medium"

    answer = result["answer"].lower()

    assert "44 lakh" in answer
    assert "13 months" in answer
    assert "6 october" in answer
    assert "not a live runway estimate" in answer


def test_latest_ceo_voice_notes_are_summarized_with_caveats():
    result = answer_ceo_question(
        "What should I worry about from the latest CEO voice notes?"
    )

    assert result["status"] == "answered"
    assert result["confidence"] == "Low"
    answer = result["answer"].lower()
    assert "marketing reporting change" in answer
    assert "private slack messages" in answer
    assert "auto-transcribed" in answer
    assert "not independently" in answer
    assert len(result["evidence"]) == 3
    assert {
        item["source"] for item in result["evidence"]
    } == {
        "T6b_CEO_Voice_Note.docx",
        "T6c_CEO_Voice_Note.docx",
        "T6d_CEO_Voice_Note.docx",
    }


def test_ceo_voice_note_summary_requires_all_three_notes():
    from app.cockpit.answer_engine import filter_topic_evidence

    results = retrieve_topic_evidence("ceo_voice_notes")
    assert len(filter_topic_evidence("ceo_voice_notes", results)) == 3

    incomplete = [
        item for item in results
        if item["source_file"] != "T6c_CEO_Voice_Note.docx"
    ]
    assert filter_topic_evidence("ceo_voice_notes", incomplete) == []


def test_ceo_voice_note_question_variations_are_recognized():
    for question in [
        "What should I worry about from the latest CEO voice notes?",
        "Summarize the CEO voice notes.",
        "What concerns are in the latest CEO voice note?",
    ]:
        assert identify_topic(question) == "ceo_voice_notes"

def test_engineering_delivery_risk_question_variations_are_recognized():
    questions = [
        "What is the engineering delivery risk?",
        "What is our delivery risk?",
        "What should worry me about Atlas?",
        "Are we at risk of missing the Atlas launch?",
        "What is the current engineering capacity situation?",
    ]

    for question in questions:
        assert identify_topic(question) == "engineering_delivery_risk"
