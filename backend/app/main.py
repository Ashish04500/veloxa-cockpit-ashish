
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator

from app.cockpit.answer_engine import answer_ceo_question
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
    allow_methods=["GET", "POST"],
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



class CEOQuestionRequest(BaseModel):
    question: str = Field(min_length=1, max_length=1000)

    @field_validator("question", mode="before")
    @classmethod
    def strip_question(cls, value):
        if isinstance(value, str):
            return value.strip()
        return value


@app.post("/api/ask")
def ask_ceo_question(payload: CEOQuestionRequest):
    """Answer a supported CEO question using approved evidence."""

    try:
        return answer_ceo_question(payload.question)
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unable to answer CEO question"
        )
