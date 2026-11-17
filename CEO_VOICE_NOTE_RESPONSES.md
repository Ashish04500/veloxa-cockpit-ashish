# CEO Voice Note Responses

## T6a — Proactive Top-Three Risk Summary

### CEO's request
"When I open it, it should just tell me what to worry about. Top three."

### Response

We agree with the request. The CEO cockpit should open with a concise summary of the three highest-priority business risks instead of requiring the CEO to ask questions manually.

### What we implemented

We implemented a provisional evidence-backed risk engine and exposed it through the FastAPI endpoint:

`GET /api/risks`

The endpoint returns three ranked risks:

1. Engineering capacity and delivery risk.
2. Funding and runway watch.
3. Marketing continuity and knowledge-transfer risk.

Each risk includes:
- Priority and heuristic score.
- Impact and confidence assessment.
- Supporting evidence and source citations.
- Recommended next action.
- Explicit uncertainty and limitations.

### Why this approach

The cockpit should help the CEO make decisions without presenting assumptions as facts. Risks are ranked using impact, manually assigned urgency and the number of distinct supporting source files.

The scores are prioritisation heuristics, not probabilities. Confidence and uncertainty are displayed separately so the CEO can distinguish verified facts from possible consequences.

### Current limitation

The risk summary is currently available through the API. Automatic display when the CEO opens the frontend dashboard has not yet been implemented.

### Next implementation step

Integrate the endpoint into the dashboard so the top three risks appear automatically on opening, with evidence and recommended actions available for review.

### Product decision

We will prioritise a proactive top-three risk summary, but will not generate warnings unsupported by available evidence. Where evidence is incomplete or conflicting, the cockpit must communicate that uncertainty rather than invent a conclusion.
