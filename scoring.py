# scoring.py

def calculate_score(signals: dict) -> dict:
    score = 0
    strengths = []
    gaps = []

    # Initiative
    if signals.get("initiative") == "yes":
        score += 2
        strengths.append("initiative")
    else:
        gaps.append("initiative")

    # Metrics
    if signals.get("metrics") == "yes":
        score += 2
        strengths.append("metrics")
    else:
        gaps.append("metrics")

    # User Research
    user_research = signals.get("user_research")
    if user_research == "full":
        score += 2
        strengths.append("user_research")
    elif user_research == "partial":
        score += 1
        gaps.append("user_research (partial)")
    else:
        gaps.append("user_research")

    # PM Level Mapping
    if score <= 2:
        level = "Beginner PM"
    elif score <= 4:
        level = "Associate PM"
    elif score <= 6:
        level = "Mid-level PM"
    else:
        level = "Senior PM"

    return {
        "score": score,
        "level": level,
        "strengths": strengths,
        "gaps": gaps
    }
