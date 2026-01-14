from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel

from auth.api_key_auth import validate_api_key
from limits.usage_limits import check_usage

from core.scoring import (
    calculate_base_score,
    calculate_signal_score,
    calculate_total_score,
    recommend_pm_archetypes
)
from core.classification import classify_pm_readiness
from core.gap_analysis import analyze_skill_gaps
from core.roadmap import build_transition_roadmap

from data.role_skill_map import ROLE_SKILL_BASE_SCORE
from data.signal_defs import SIGNALS
from data.pm_archetypes import PM_ARCHETYPES
from data.archetype_skill_needs import ARCHETYPE_SKILL_NEEDS

from agents.reasoning_agent import reasoning_agent
from agents.signal_agent import signal_agent
from agents.roadmap_agent import roadmap_agent
from agents.guidance_agent import guidance_agent


app = FastAPI(title="PM Path Finder API")


class AnalysisRequest(BaseModel):
    role: str
    signals: dict
    target_pm_role: str


@app.post("/analyze")
def analyze(
    request: AnalysisRequest,
    plan: str = Depends(validate_api_key)
):
    api_key = request.role + "_key"  # simple placeholder

    if not check_usage(api_key, plan):
        raise HTTPException(status_code=403, detail="Usage limit exceeded")

    role = request.role.lower()

    if role not in ROLE_SKILL_BASE_SCORE:
        raise HTTPException(status_code=400, detail="Unsupported role")

    base_total, base_breakdown = calculate_base_score(
        role, ROLE_SKILL_BASE_SCORE
    )

    signal_score = calculate_signal_score(request.signals)
    total_score = calculate_total_score(base_total, signal_score)
    readiness = classify_pm_readiness(total_score)

    system_paths = recommend_pm_archetypes(
        base_breakdown, request.signals, PM_ARCHETYPES
    )

    risk = (
        "Low"
        if request.target_pm_role in [a[0] for a in system_paths]
        else "High"
    )

    gaps = analyze_skill_gaps(
        base_breakdown,
        request.target_pm_role,
        ARCHETYPE_SKILL_NEEDS
    )

    roadmap = build_transition_roadmap(gaps, risk)

    return {
        "readiness": readiness,
        "total_score": total_score,
        "system_paths": system_paths,
        "risk": risk,
        "gaps": gaps,
        "reasoning": reasoning_agent({
            "role": role,
            "readiness": readiness,
            "score": total_score
        }),
        "signal_analysis": signal_agent(request.signals),
        "roadmap": roadmap_agent(roadmap),
        "guidance": guidance_agent(risk, request.target_pm_role)
    }
