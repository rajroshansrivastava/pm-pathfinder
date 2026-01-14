from openai import OpenAI

try:
    from prod_config import OPENAI_API_KEY
except Exception:
    from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def roadmap_agent(roadmap_steps):
    prompt = f"""
Convert this PM transition roadmap into weekly, actionable steps.

Rules:
- Concrete actions
- No fluff

Roadmap:
{roadmap_steps}
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return response.output_text
