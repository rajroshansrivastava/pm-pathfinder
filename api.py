from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from scoring import evaluate_pm
from ai_reasoning import generate_reasoning

app = FastAPI(title="PM Path Finder API")

API_KEYS = {"free-key-123"}


class AnalysisRequest(BaseModel):
    role: str
    signals: dict
    target_pm_role: str


@app.get("/")
def root():
    return {"message": "PM Path Finder API is running"}


@app.post("/analyze")
def analyze(
    payload: AnalysisRequest,
    x_api_key: str = Header(...)
):
    if x_api_key not in API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API key")

    analysis = evaluate_pm(
        payload.signals,
        payload.target_pm_role
    )

    reasoning = generate_reasoning(
        role=payload.role,
        target_pm_role=payload.target_pm_role,
        score=analysis["score"],
        level=analysis["level"],
        strengths=analysis["strengths"],
        gaps=analysis["gaps"]
    )

    return {
        "status": "success",
        "input_role": payload.role,
        "target_pm_role": payload.target_pm_role,
        "analysis": analysis,
        "ai_reasoning": reasoning
    }
