from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from typing import Dict
import os
import openai

# -----------------------
# App setup
# -----------------------

app = FastAPI(
    title="PM Path Finder API",
    version="0.1.0"
)

# -----------------------
# Security
# -----------------------

VALID_API_KEYS = ["free-key-123"]

# -----------------------
# OpenAI setup
# -----------------------

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY not set")

openai.api_key = OPENAI_API_KEY

# -----------------------
# Request model
# -----------------------

class AnalysisRequest(BaseModel):
    role: str
    signals: Dict[str, str]
    target_pm_role: str

# -----------------------
# Root endpoint
# -----------------------

@app.get("/")
def root():
    return {
        "message": "PM Path Finder API is running"
    }

# -----------------------
# Analyze endpoint (AI POWERED)
# -----------------------

@app.post("/analyze")
def analyze(
    data: AnalysisRequest,
    x_api_key: str = Header(...)
):
    # --- API key validation ---
    if x_api_key not in VALID_API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API key")

    # --- Prepare prompt for OpenAI ---
    prompt = f"""
You are a senior product leader and career coach.

Analyze the following candidate:

Current Role: {data.role}
Target PM Role: {data.target_pm_role}

Signals:
{data.signals}

Your task:
1. Assess PM readiness (score 0–10)
2. Classify level (Beginner / Mid / Senior PM)
3. Identify strengths
4. Identify gaps
5. Give next-step advice (concise, practical)

Respond in JSON with keys:
score, level, strengths, gaps, advice
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert PM career advisor."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4
        )

        ai_output = response.choices[0].message.content

        return {
            "status": "success",
            "input": data.dict(),
            "ai_analysis": ai_output
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
