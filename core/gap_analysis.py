def analyze_skill_gaps(current_skills, target_archetype, archetype_needs):
    gaps = {}

    if target_archetype not in archetype_needs:
        return gaps

    required = archetype_needs[target_archetype]

    for skill, required_level in required.items():
        current_level = current_skills.get(skill, 0)

        if current_level < required_level:
            gaps[skill] = {
                "current": current_level,
                "required": required_level,
                "gap": required_level - current_level
            }

    return gaps
