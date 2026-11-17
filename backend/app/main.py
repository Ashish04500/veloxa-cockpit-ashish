
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.cockpit.risk_engine import get_top_risks

app = FastAPI(
    title="Veloxa CEO Cockpit API",
    description="Evidence-backed CEO risk intelligence",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
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

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unable to generate risk summary"
        )
