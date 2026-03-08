Candidate: Timothy Holt

Scenario: Community Safety & Digital Wellness

App Name: SignalSafe AI

### Overview
SignalSafe AI is a Flask web app that helps community members review safety incident reports and generate a plain-language digest summarizing key concerns and recommended actions. The app is designed with simplicity and reliability in mind, targeting non-technical users including elderly community members, and neighborhood groups/members.

### Design:
- The core design goal was to build a complete, demoable app within the 4-6 hour timeframe without sacrificing functionality.
- For the frontend, a Flask app with Jinja2 templates was chosen over React because it eliminated build overhead, kept the codebase a single language, and was fast to iterate/test on (no API layer or state management to maintain).
- I chose SQLite for the database because it required zero setup, ships with Python's standard library, and was best for a local demo using synthetic data.
- The synthetic dataset is a JSON file (data/sample_reports.json) containing 13 safety incidents seeded into the database on first run. Each record includes a title, description, category (one of: phishing, phone_scam, data_breach, fraud, physical_safety, utility_scam), severity (low, medium, or high), location, status (new, reviewed, or resolved), an ISO 8601 created_at timestamp, and a verified boolean. The dataset is intentionally varied across all category and severity combinations to make filtering and digest generation meaningful during the demo.
- The AI capability was intentionally scoped to a single function (digest/summary generation).
- The fallback digest/summary uses deterministic rule-based logic tied to report categories, so the app always produces a useful output regardless of API availability.

### Tech Stack:
I wanted every component in my stack to be lightweight, well-documented, and fast to set up. There are no external services, no database servers, and no build steps required to run the app locally.
- The backend is Python 3.10 with Flask as the web framework and Jinja2 for server-side HTML templating.
- The database is SQLite accessed via Python's built-in sqlite3 module with no ORM.
- Environment variables are managed with python-dotenv.
- AI digest generation uses the OpenAI Python SDK calling gpt-3.5-turbo.
- The test suite uses pytest.
- The frontend is HTML and CSS with no JavaScript framework.

### Future Enhancements:
- Adding user authentication so report submissions and status updates are tied to verified identities rather than anaonymous/open to anyone.
- A heat map visualization showing report locations geographically would help neighborhood groups and elderly users to identify clusters of incidents in specific areas.
- On the AI side, allowing users to ask follow-up questions about the digest rather than receiving a static summary would make the feature more useful.
- Replacing SQLite with PostgreSQL would be necessary before production deployment to support concurrent users.
- Adding pagination to the reports list would improve performance as the dataset grows.
- Adding Email notifications through an API for high-severity verified reports to alert opted-in members in real time of potential threats.
