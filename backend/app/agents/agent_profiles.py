
from employee_roster import load_employee_agents


def build_agent_profiles():
    employees = load_employee_agents()

    profiles = []

    for employee in employees:
        profile = {
            "employee_id": employee["Emp ID"],
            "name": employee["Full Name"],
            "email": employee["Work Email"],
            "department": employee["Department"],
            "role": employee["Title"],
            "manager_id": employee["Manager ID"],
            "join_date": employee["Join Date"],
            "location": employee["Location"],
            "employment_status": employee["Status"],

            "verified_facts": [
                "Employee identity and role are taken from Employee_Master.xlsx"
            ],

            "work_context": [],
            "personal_life": {
                "details": [],
                "is_assumed": True
            },

            "assumptions": [],
            "evidence_sources": [
                {
                    "file": "Employee_Master.xlsx",
                    "field": "Employee identity and employment details"
                }
            ]
        }

        profiles.append(profile)

    return profiles


if __name__ == "__main__":
    profiles = build_agent_profiles()

    print("PROFILES CREATED:", len(profiles))

    for profile in profiles:
        print(
            profile["employee_id"],
            "|",
            profile["name"],
            "|",
            profile["role"]
        )
