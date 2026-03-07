import os
from .ai_service import generate_ai_digest

CATEGORY_ADVICE = {
    'phishing': 'Do not click suspicious links in texts or emails. Verify the sender before responding.',
    'phone_scam': 'Hang up on unsolicited callers asking for personal information or payment.',
    'data_breach': 'Change your passwords immediately and enable two-factor authentication where possible.',
    'fraud': 'Never pay upfront to unknown contractors or services. Verify credentials before hiring.',
    'physical_safety': 'Stay aware of your surroundings and report suspicious activity to local authorities.',
    'utility_scam': 'Verify payment demands by calling your utility provider directly using their official number.'
}

def build_fallback_digest(reports):
    total = len(reports)
    category_counts = {}
    high_verified = []

    for r in reports:
        cat = r['category']
        category_counts[cat] = category_counts.get(cat, 0) + 1
        if r['severity'] == 'high' and r['verified']:
            high_verified.append(r['title'])

    top_categories = sorted(category_counts, key=category_counts.get, reverse=True)[:2]
    top_names = ' and '.join(top_categories).replace('_', ' ')

    summary = (
        f"There are {total} relevant safety reports, with {top_names} appearing most often."
    )
    if high_verified:
        summary += f" {len(high_verified)} high-severity verified incident(s) may require prompt attention."

    what_matters = []
    for cat in top_categories:
        matching = [r['title'] for r in reports if r['category'] == cat]
        if matching:
            what_matters.append(f"{cat.replace('_', ' ').title()}: {matching[0]}")

    what_to_do = []
    seen_categories = set()
    for r in reports:
        cat = r['category']
        if cat not in seen_categories and cat in CATEGORY_ADVICE:
            what_to_do.append(CATEGORY_ADVICE[cat])
            seen_categories.add(cat)

    return {
        'source': 'fallback',
        'summary': summary,
        'what_matters': what_matters,
        'what_to_do': what_to_do,
        'report_count': total
    }

def generate_digest(reports):
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key:
        try:
            result = generate_ai_digest(reports)
            result['source'] = 'ai'
            result['report_count'] = len(reports)
            return result
        except Exception:
            pass
    return build_fallback_digest(reports)
