from openai import OpenAI

try:
    from prod_config import OPENAI_API_KEY
except Exception:
    from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def signal_agent(signals):
    prompt = f"""
You are analyzing PM behavioral signals.

Rules:
- No assumptions
- Highlight strengths, gaps, missing proof

Signals:
{signals}
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return response.output_text
