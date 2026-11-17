
from fastapi import FastAPI, HTTPException
from app.cockpit.risk_engine import get_top_risks

app = FastAPI(
    title="Veloxa CEO Cockpit API",
    description="Evidence-backed CEO risk intelligence",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Veloxa CEO Cockpit API is running",
        "status": "healthy"
    }


@app.get("/api/risks")
def read_top_risks():
    """Return the current evidence-backed top-three CEO risks."""

    try:
        risks = get_top_risks()

        return {
            "count": len(risks),
            "risks": risks
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to generate risk summary: {str(error)}"
        )
