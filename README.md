# SignalSafe AI

**Candidate:** Timothy Holt

**Scenario:** Community Safety & Digital Wellness

**Estimated Time Spent:** ~5 hours

---

## Quick Start:

### Prerequisites
- Python 3.10+
- pip
- virtualenv

### Run Commands
```bash
git clone https://github.com/timholt77/panw-case-study.git
cd panw-case-study
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Add your OPENAI_API_KEY to .env
python3 run.py
```
Then open http://127.0.0.1:5000 in your browser.

### Test Commands
```bash
pytest tests/ -v
```

---

## AI Disclosure:

### Did you use an AI assistant (Copilot, ChatGPT, etc.)? (Yes/No)
Yes, I used Anthropic's Claude Sonnet 4.6.

### How did you verify the suggestions?
I treated AI suggestions as a starting point rather than final code. I verified AI-generated code by implementing changes incrementally and testing each piece in isolation before integrating it into the app. For AI-generated database code, I ran direct Python test commands locally to confirm seeding, querying, and filtering worked correctly. For the OpenAI integration, I tested the full request/response flow end to end and confirmed the fallback path worked correctly when no API key was present or the API call failed. After integrating all AI-generated code, I ran the full pytest suite to confirm all 25 tests passed and used the web UI to manually validate user flows, edge cases, and error handling within the web app itself.

### Give one example of a suggestion you rejected or changed:
One suggestion I rejected was the initial recommendation to use a more frontend-heavy stack with React. I chose Flask with server-rendered templates instead because it was a better fit for the 4–6 hour case-study time limit, and let me spend more time on backend quality, data flow, testing, and AI/fallback behavior instead of build tooling and frontend setup. I also changed suggestions that tried to broaden the app's scope. For example, rather than adding authentication, or more advanced AI features, I kept the AI component focused on digest summarization. That decision made the app more reliable, easier to test, and helped me focus on providing high quality features for a subset of chosen features.

---

## Tradeoffs & Prioritization:

### What did you cut to stay within the 4–6 hour limit?
I wanted to add a heat map visualization feature so that users of the app could visually see if there were regions where more reports were being submitted from, but did not have time. I believed this feature could have been useful for the target audience of Elderly Users as visualizations can be easier to ascertain information from quickly if you have an impairment or disability compared to the provided AI generated digest summary which can be somewhat text heavy. I also believed this feature could have been useful for the target audience of Neighborhood Groups as it would allow a visual representation of whether their neighboorhood was being targeted at a higher rate, and coupled with the AI summary in the digest tab would empower them with information to take action against security threats.

### What would you build next if you had more time?
I would add user authentication to the web app so report submissions would be tied to specific users rather than open to submission from anyone. I would add a heat map visualization showing report locations geographically which would be useful for identifying neighborhoods with frequently occurring reported incidents. I  would integrate an email notification API for sending notifications of high-severity verified reports to community members who opt in. On the AI side, I might add a feature to let users interact and ask follow-up questions to the AI agent about the digest rather than only providing a static summary. 

### Known limitations:
- No user authentication (anyone can submit a report without being identified, creates opportunities for risk because there is less accountability associated with being anonymous)
- If users submit reports through the app that are vague, lacking in information, or sparse the AI will create a lower quality summary of the reports in the digest tab which could be unhelpful
- Performance of the app would degrade as the number of reports increases. The application does not currently support pagination (so if there were 500 security reports they would all appear on one long page instead of being split across multiple pages). The app loads all reports in a single database query with no limit, which would cause slow page loads and poor user experience as the number of reports grows
- Web app is local with no deployment configuration for production hosting currently

---

## Demo Video

[Link to demo video](YOUR_VIDEO_LINK_HERE)


