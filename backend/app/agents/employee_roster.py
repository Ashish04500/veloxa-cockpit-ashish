
from pathlib import Path
import sys

BACKEND_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BACKEND_DIR / "app"))

from ingestion.file_reader import read_file

ROOT = Path(__file__).resolve().parents[3]

EMPLOYEE_FILE = (
    ROOT
    / "data"
    / "raw"
    / "Veloxa_Hackathon_Release_Packs"
    / "Day1_Mon_16Nov"
    / "data_room"
    / "hr"
    / "Employee_Master.xlsx"
)

TARGET_DEPARTMENTS = {
    "Engineering",
    "Finance",
    "People & Ops",
    "Marketing"
}


def load_employee_agents():
    data = read_file(EMPLOYEE_FILE)
    employees = data["Employees"]

    agents = [
        employee
        for employee in employees
        if employee.get("Department") in TARGET_DEPARTMENTS
    ]

    if len(agents) != 14:
        raise ValueError(
            f"Expected 14 agents, found {len(agents)}"
        )

    return agents


if __name__ == "__main__":
    agents = load_employee_agents()

    print("TOTAL AGENTS:", len(agents))

    for agent in agents:
        print(
            agent["Emp ID"],
            "|", agent["Full Name"],
            "|", agent["Title"],
            "|", agent["Department"],
            "|", agent["Status"]
        )
