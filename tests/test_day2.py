
import sys
from pathlib import Path

BACKEND_APP = Path(__file__).resolve().parents[1] / "backend" / "app"
sys.path.insert(0, str(BACKEND_APP))

from agents.agent_profiles import build_agent_profiles


def get_profiles():
    return build_agent_profiles()


# Basic profile checks

def test_exactly_14_employee_profiles():
    assert len(get_profiles()) == 14


def test_employee_ids_are_unique():
    profiles = get_profiles()
    ids = [p["employee_id"] for p in profiles]
    assert len(ids) == len(set(ids))


def test_all_profiles_have_identity():
    for profile in get_profiles():
        assert profile["name"]
        assert profile["role"]
        assert profile["department"]


def test_verified_context_has_evidence():
    for profile in get_profiles():
        for item in profile["work_context"]:
            assert item["detail"]
            assert item["source"]
            assert item["confidence"] in ["high", "medium", "low"]


def test_siddharth_resignation_is_recorded():
    profiles = get_profiles()
    siddharth = next(
        p for p in profiles if p["employee_id"] == "VX013"
    )

    assert any(
        "resignation" in fact.lower()
        for fact in siddharth["verified_facts"]
    )


def test_unverified_hiring_claim_has_low_confidence():
    profiles = get_profiles()
    rohan = next(
        p for p in profiles if p["employee_id"] == "VX015"
    )

    assert any(
        item["confidence"] == "low"
        for item in rohan["work_context"]
    )


def test_no_personal_life_details_are_invented():
    for profile in get_profiles():
        assert profile["personal_life"]["details"] == []


def test_every_profile_has_evidence_sources():
    for profile in get_profiles():
        assert len(profile["evidence_sources"]) >= 1


# Evidence accuracy checks

def test_department_pulse_is_not_assigned_to_individual_performance():
    profiles = get_profiles()

    for employee_id in ["VX005", "VX006"]:
        profile = next(
            p for p in profiles
            if p["employee_id"] == employee_id
        )

        for item in profile["work_context"]:
            if "pulse" in item["detail"].lower():
                assert "team" in item["detail"].lower()


def test_vikram_has_no_personal_pulse_score():
    profiles = get_profiles()
    vikram = next(
        p for p in profiles if p["employee_id"] == "VX004"
    )

    assert not any(
        "pulse" in item["detail"].lower()
        for item in vikram["work_context"]
    )


def test_siddharth_is_not_directly_linked_to_req016():
    profiles = get_profiles()
    siddharth = next(
        p for p in profiles if p["employee_id"] == "VX013"
    )

    assert not any(
        "REQ-016" in item["detail"]
        for item in siddharth["work_context"]
    )
