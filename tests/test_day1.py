
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"

sys.path.insert(0, str(BACKEND / "app"))

from agents.employee_roster import load_employee_agents
from ingestion.file_reader import read_file


DATA_FILE = ROOT / "data" / "processed" / "day1_documents.jsonl"


def load_documents():
    with DATA_FILE.open(encoding="utf-8") as file:
        return [json.loads(line) for line in file]


def test_day1_has_15_documents():
    assert len(load_documents()) == 15


def test_all_day1_documents_ingested_successfully():
    documents = load_documents()
    assert all(doc["status"] == "success" for doc in documents)


def test_day1_has_no_duplicate_source_paths():
    documents = load_documents()
    paths = [doc["source_path"] for doc in documents]
    assert len(paths) == len(set(paths))


def test_employee_master_has_19_records():
    path = (
        ROOT / "data/raw/Veloxa_Hackathon_Release_Packs/"
        "Day1_Mon_16Nov/data_room/hr/Employee_Master.xlsx"
    )
    data = read_file(path)
    assert len(data["Employees"]) == 19


def test_exactly_14_target_agents_exist():
    agents = load_employee_agents()
    assert len(agents) == 14


def test_agent_employee_ids_are_unique():
    agents = load_employee_agents()
    ids = [agent["Emp ID"] for agent in agents]
    assert len(ids) == len(set(ids))


def test_agent_departments_are_valid():
    agents = load_employee_agents()
    allowed = {"Engineering", "Finance", "People & Ops", "Marketing"}
    assert all(agent["Department"] in allowed for agent in agents)


def test_agent_profiles_include_notice_period_employee():
    agents = load_employee_agents()
    siddharth = [
        agent for agent in agents
        if agent["Emp ID"] == "VX013"
    ]
    assert len(siddharth) == 1
    assert siddharth[0]["Status"] == "Notice period"


def test_board_pdfs_have_extractable_text():
    documents = load_documents()
    board_files = [
        doc for doc in documents
        if doc["source_file"].startswith("Board_Update_")
    ]
    assert len(board_files) == 2
    assert all(
        sum(len(page["text"]) for page in doc["content"]) > 100
        for doc in board_files
    )


def test_entity_resolution_template_is_preserved():
    documents = load_documents()
    record = next(
        doc for doc in documents
        if doc["source_file"] == "Entity_Resolution.xlsx"
    )
    assert "Entities" in record["content"]
    assert record["content"]["Entities"] == []
