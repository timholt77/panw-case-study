import os
import json
from openai import OpenAI

def generate_ai_digest(reports):
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError('No API key set')

    client = OpenAI(api_key=api_key)

    report_text = ''
    for r in reports:
        report_text += (
            f"- Title: {r['title']}\n"
            f"  Category: {r['category']}\n"
            f"  Severity: {r['severity']}\n"
            f"  Verified: {bool(r['verified'])}\n"
            f"  Description: {r['description']}\n\n"
        )

    prompt = f"""You are generating a calm, actionable community safety digest from synthetic incident reports.

Rules:
- Be concise and reassuring.
- Prioritize verified and high-severity incidents.
- Do not exaggerate risk.
- Use simple language suitable for elderly users.
- Focus on practical steps.

Return ONLY a JSON object with these exact keys:
- summary: a short paragraph summarizing the situation
- what_matters: a list of 2-3 short strings highlighting key concerns
- what_to_do: a list of 2-4 short actionable steps

Reports:
{report_text}"""

    response = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[{'role': 'user', 'content': prompt}],
        max_tokens=600
    )

    content = response.choices[0].message.content
    clean = content.replace('```json', '').replace('```', '').strip()
    return json.loads(clean)
