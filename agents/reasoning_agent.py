from openai import OpenAI

try:
    from prod_config import OPENAI_API_KEY
except Exception:
    from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def reasoning_agent(context):
    prompt = f"""
You are a PM career reasoning assistant.

Rules:
- Do NOT change scores
- Do NOT invent facts
- ONLY explain logic already computed

Context:
{context}

Explain clearly and concisely.
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return response.output_text
