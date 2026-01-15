import os
from fastapi import FastAPI, Header, HTTPException, Depends
from pydantic import BaseModel

# -------------------------------------------------
# App
# -------------------------------------------------

app = FastAPI(
    title="PM Path Finder API",
    version="0.1.0"
)

# -------------------------------------------------
# API KEY AUTH
# -------------------------------------------------

DEFAULT_API_KEY = os.environ.get("DEFAULT_API_KEY")

if not DEFAULT_API_KEY:
    raise RuntimeError("DEFAULT_API_KEY is not set in environment variables")


def verify_api_key(
    x_api_key: str = Header(..., alias="x-api-key")
):
    if x_api_key != DEFAULT_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key


# -------------------------------------------------
# Request Model
# -------------------------------------------------

class AnalysisRequest(BaseModel):
    role: str
    signals: dict
    target_pm_role: str


# -------------------------------------------------
# Health Check
# -------------------------------------------------

@app.get("/")
def root():
    return {"status": "PM Path Finder API running"}


# -------------------------------------------------
# Main API
# -------------------------------------------------

@app.post("/analyze")
def analyze(
    payload: AnalysisRequest,
    _: str = Depends(verify_api_key)
):
    return {
        "status": "success",
        "message": "API key accepted",
        "data": {
            "role": payload.role,
            "signals": payload.signals,
            "target_pm_role": payload.target_pm_role
        }
    }
