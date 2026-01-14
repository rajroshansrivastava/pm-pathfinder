def calculate_base_score(role, role_skill_map):
    if role not in role_skill_map:
        raise ValueError("Role not supported yet")

    scores = role_skill_map[role]
    total = sum(scores.values())
    return total, scores


def calculate_signal_score(signal_inputs):
    score = 0
    for signal, value in signal_inputs.items():
        if value == "yes":
            score += 3
        elif value == "partial":
            score += 1
    return score


def calculate_total_score(base, signal):
    return round((base * 0.6) + (signal * 0.4), 2)


def recommend_pm_archetypes(base_breakdown, signal_inputs, archetypes):
    recommendations = []

    for archetype, details in archetypes.items():
        score = 0

        for strength in details["required_strengths"]:
            if strength in base_breakdown and base_breakdown[strength] >= 3:
                score += 1

            if strength == "ambiguity_handling":
                if signal_inputs.get("ambiguity_signal") == "yes":
                    score += 1

        recommendations.append((archetype, score, details["description"]))

    recommendations.sort(key=lambda x: x[1], reverse=True)
    return recommendations[:2]
