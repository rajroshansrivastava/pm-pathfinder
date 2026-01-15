from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_reasoning(
    role: str,
    target_pm_role: str,
    score: int,
    level: str,
    strengths: list,
    gaps: list
):
    prompt = f"""
You are a senior product mentor.

A user currently works as: {role}
Target PM role: {target_pm_role}

Evaluation results:
- Score: {score}
- Level: {level}
- Strengths: {strengths}
- Gaps: {gaps}

Explain in simple language:
1. Why the user got this score
2. What they are doing well
3. What they should improve next
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful PM career mentor."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5
    )

    return response.choices[0].message.content
