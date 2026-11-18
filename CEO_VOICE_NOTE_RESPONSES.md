
# CEO Voice Note Responses

## T6a — Proactive Top-Three Risk Summary

### CEO's request
"When I open it, it should just tell me what to worry about. Top three."

### Response

The CEO cockpit now automatically displays a concise summary of the three highest-priority business risks when the frontend dashboard opens.

### What we implemented

We implemented an evidence-backed risk engine and exposed it through the FastAPI endpoint:

`GET /api/risks`

The React frontend automatically fetches this endpoint on opening and displays three ranked risks:

1. Engineering capacity and delivery risk.
2. Funding and runway watch.
3. Marketing continuity and knowledge-transfer risk.

Each risk includes:
- Priority and heuristic score.
- Impact and confidence assessment.
- Supporting evidence and source citations.
- Recommended next action.
- Explicit uncertainty and limitations.

The dashboard also includes:
- Summary metrics for priority risks, high-impact risks and evidence sources.
- Expandable evidence sections.
- Manual refresh functionality.
- API connection status and error handling.
- Last-updated timestamp.

### Verification

- Backend API successfully returns three risk records.
- Frontend successfully retrieves and displays all three risks.
- Evidence sections expand and show supporting records.
- API disconnection displays an error and changes the status indicator.
- API reconnection restores successful loading.
- ESLint passes.
- Vite production build passes.

### Why this approach

The cockpit should help the CEO make decisions without presenting assumptions as facts. Risks are ranked using impact, manually assigned urgency and the number of distinct supporting source files.

The scores are prioritisation heuristics, not probabilities. Confidence and uncertainty are displayed separately so the CEO can distinguish verified facts from possible consequences.

### Current limitations

- Risk scoring is heuristic rather than statistically calibrated.
- The dashboard currently displays the latest risk summary returned by the API; historical point-in-time filtering is not yet fully implemented.
- API connection status reflects the latest request, not continuous real-time monitoring.

### Product decision

We will prioritise a proactive top-three risk summary, but will not generate warnings unsupported by available evidence. Where evidence is incomplete or conflicting, the cockpit must communicate that uncertainty rather than invent a conclusion.


## T6b — Planned Marketing Reporting Change

### CEO's statement

The CEO stated that Marketing would report to a new CRO from "next month. Or the month after", indicating that the transition date was still being finalised.

### Response

The cockpit should treat this as a planned organisational change, not a completed reporting-line update.

The available voice note does not establish:
- The identity of the incoming CRO.
- The exact effective date.
- Whether the change has received final approval.
- Whether any interim reporting arrangement applies.

The current reporting structure should therefore remain unchanged until an authoritative confirmation is available.

### Recommended cockpit behaviour

1. Record the proposed Marketing reporting change as a pending organisational event.
2. Preserve the existing reporting relationship as the current confirmed structure.
3. Request confirmation of the new CRO's identity, approval status and effective date.
4. Once confirmed, record the new reporting relationship with its effective date.
5. Retain the previous relationship so historical reporting structures can be reconstructed for earlier periods.

### Evidence and confidence

**Source:** T6b_CEO_Voice_Note.docx.

**Confidence:** High that a reporting change is planned. Low regarding its exact timing and implementation details.

The phrase "next month. Or the month after" is explicitly uncertain and must not be converted into a definite date.

### Current implementation status

The current cockpit does not yet provide a complete effective-dated organisational history feature. This is a recommended product requirement, not a verified existing capability.

Until implemented, the system must not silently overwrite current employee-manager relationships based on this voice note.

### Product decision

Organisational changes must be represented with effective dates and retained history. The cockpit should distinguish proposed, approved and effective changes, preventing future organisational plans from being presented as current facts.
