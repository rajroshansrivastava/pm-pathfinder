def build_transition_roadmap(gaps, risk_level):
    roadmap = []

    if not gaps:
        roadmap.append("You already meet core requirements for this PM path.")
        roadmap.append("Focus on execution, storytelling, and interviews.")
        return roadmap

    roadmap.append("FOUNDATION PHASE (0–3 months):")
    for skill in gaps:
        roadmap.append(f"- Build fundamentals in {skill}")

    roadmap.append("\nAPPLICATION PHASE (3–6 months):")
    roadmap.append("- Apply skills in real or simulated projects")
    roadmap.append("- Collect proof of ownership and decisions")

    if risk_level == "High":
        roadmap.append("\nRISK MITIGATION:")
        roadmap.append("- Maintain a fallback PM path")
        roadmap.append("- Extend timeline by 6–9 months")

    roadmap.append("\nAVOID:")
    roadmap.append("- Tool-first learning")
    roadmap.append("- Random certifications")
    roadmap.append("- Blind PM applications")

    return roadmap
