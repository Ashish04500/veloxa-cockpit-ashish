
try:
    from .employee_roster import load_employee_agents
except ImportError:
    from employee_roster import load_employee_agents


# Evidence-backed context from Day 1 and Day 2.
# Employee IDs are used to avoid matching people by name alone.

EMPLOYEE_CONTEXT = {

    "VX003": {
        "verified_facts": [
            "CFO, identified in Employee_Master.xlsx",
            "Sent an email approving the pause of REQ-014 and REQ-015 on 12 August 2026"
        ],
        "work_context": [
            {
                "detail": "Prioritised burn control by pausing two Engineering hiring requisitions",
                "source": "Day2 data_room/email/06.eml",
                "confidence": "high"
            }
        ]
    },

    "VX004": {
        "verified_facts": [
            "VP Engineering, identified in Employee_Master.xlsx",
            "Acknowledged the pause of REQ-014 and REQ-015 on 12 August 2026"
        ],
        "work_context": [
            {
                "detail": "Agreed to absorb the work after two Engineering roles were paused",
                "source": "Day2 data_room/email/07.eml",
                "confidence": "high"
            }
        ]
    },

    "VX005": {
        "verified_facts": [
            "Head of People & Ops, identified in Employee_Master.xlsx",
            "Sent the CEO an email noting the Engineering pulse decline and recommending manager 1:1s"
        ],
        "work_context": [
            {
                "detail": "Engineering team pulse score was 3.1 in the latest survey, with 4 responses from a team of 5",
                "source": "Day2 data_room/hr/Pulse_Survey.xlsx",
                "confidence": "high"
            },
            {
                "detail": "Recommended that the CEO not receive individual survey comments because the team is too small",
                "source": "Day2 data_room/email/11.eml",
                "confidence": "high"
            }
        ]
    },

    "VX006": {
        "verified_facts": [
            "Head of Marketing, identified in Employee_Master.xlsx"
        ],
        "work_context": [
            {
                "detail": "Marketing team aggregate pulse score was 3.4 in the latest survey",
                "source": "Day2 data_room/hr/Pulse_Survey.xlsx",
                "confidence": "high"
            },
            {
                "detail": "Marketing team aggregate pulse score declined from 3.8 in the previous quarter",
                "source": "Day2 data_room/hr/Pulse_Survey.xlsx",
                "confidence": "high"
            }
        ]
    },

    "VX009": {
        "verified_facts": [
            "Senior Frontend Engineer, identified in Employee_Master.xlsx",
            "Requested a permanent remote arrangement while remaining available for monthly Bengaluru visits"
        ],
        "work_context": [
            {
                "detail": "Reported that working from Pune had worked well and requested permanent remote status; approval is not confirmed",
                "source": "Day2 data_room/email/10.eml",
                "confidence": "high"
            }
        ]
    },

    "VX013": {
        "verified_facts": [
            "Product Marketing Manager, identified in Employee_Master.xlsx",
            "Submitted resignation dated 15 September 2026",
            "Stated last working day as 31 October 2026"
        ],
        "work_context": [
            {
                "detail": "Resignation letter cited unclear launch timelines and work not reaching customers",
                "source": "Day2 data_room/documents/Resignation_Letter_SM.pdf",
                "confidence": "high"
            }
        ]
    },

    "VX015": {
        "verified_facts": [
            "Talent Partner, identified in Employee_Master.xlsx"
        ],
        "work_context": [
            {
                "detail": "A machine-generated Head of People call transcript attributes figures of 22 open roles in April, six lost roles in August and offer acceptance in the 50s to Rohan; these figures are ambiguous and have not been independently verified",
                "source": "Day2 transcripts/T3_Head_of_People_Call.docx",
                "confidence": "low"
            }
        ]
    }
}


def build_agent_profiles():
    employees = load_employee_agents()

    profiles = []

    for employee in employees:

        employee_id = employee["Emp ID"]
        context = EMPLOYEE_CONTEXT.get(employee_id, {})

        profile = {
            "employee_id": employee_id,
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
            ] + context.get("verified_facts", []),

            "work_context": context.get("work_context", []),

            "personal_life": {
                "details": [],
                "is_assumed": False,
                "note": (
                    "No personal-life information has been verified. "
                    "Do not infer it from leave records."
                )
            },

            "assumptions": [],

            "evidence_sources": [
                {
                    "file": "Employee_Master.xlsx",
                    "field": "Employee identity and employment details"
                }
            ] + [
                {
                    "file": item["source"],
                    "field": item["detail"],
                    "confidence": item["confidence"]
                }
                for item in context.get("work_context", [])
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
            profile["role"],
            "| Work context:",
            len(profile["work_context"])
        )
