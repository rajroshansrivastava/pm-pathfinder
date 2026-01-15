import os
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from typing import Dict
from openai import OpenAI

# -----------------------
# App setup
# -----------------------
app = FastAPI(
    title="PM Path Finder API",
    version="0.1.0"
)

# -----------------------
# OpenAI Client (NEW SDK)
# -----------------------
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# -----------------------
# Request Schema
# -----------------------
class AnalysisRequest(BaseModel):
    role: str
    signals: Dict[str, str]
    target_pm_role: str

# -----------------------
# Root health check
# -----------------------
@app.get("/")
def root():
    return {"status": "PM Path Finder API running"}

# -----------------------
# Analyze Endpoint (AI)
# -----------------------
@app.post("/analyze")
def analyze(
    payload: AnalysisRequest,
    x_api_key: str = Header(...)
):
    # API key check
    if x_api_key != "free-key-123":
        raise HTTPException(status_code=401, detail="Invalid API key")

    # Build prompt
    prompt = f"""
You are a Product Management career advisor.

Current role: {payload.role}
Target PM role: {payload.target_pm_role}

Signals:
{payload.signals}

Analyze readiness and return:
- score (0–10)
- level
- strengths
- gaps
- advice
"""

    try:
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

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
