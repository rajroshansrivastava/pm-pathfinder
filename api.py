import os
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from typing import Dict
from openai import OpenAI

app = FastAPI(
    title="PM Path Finder API",
    version="0.1.0"
)

# Load keys from environment
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
EXPECTED_API_KEY = os.getenv("API_KEY")

client = OpenAI(api_key=OPENAI_KEY)

class AnalysisRequest(BaseModel):
    role: str
    signals: Dict[str, str]
    target_pm_role: str

@app.get("/")
def root():
    return {"status": "PM Path Finder API running"}

@app.post("/analyze")
def analyze(
    payload: AnalysisRequest,
    x_api_key: str = Header(...)
):
    if not EXPECTED_API_KEY:
        raise HTTPException(status_code=500, detail="API_KEY not set on server")

    if x_api_key != EXPECTED_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    prompt = f"""
You are a Product Management career advisor.

Current role: {payload.role}
Target PM role: {payload.target_pm_role}

Signals:
{payload.signals}

Return:
- readiness score (0–10)
- level
- strengths
- gaps
- advice
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert PM coach."},
            {"role": "user", "content": prompt}
        ]
    )

    return {
        "status": "success",
        "ai_reasoning": response.choices[0].message.content
    }
