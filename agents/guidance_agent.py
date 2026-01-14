from openai import OpenAI

try:
    from prod_config import OPENAI_API_KEY
except Exception:
    from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def guidance_agent(risk_level, target_role):
    prompt = f"""
You are a brutally honest PM mentor.

Target PM Role: {target_role}
Risk Level: {risk_level}

Give:
- Clear risks
- What NOT to do
- Next 3 actions
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return response.output_text
