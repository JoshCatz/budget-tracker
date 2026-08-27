

Readme · MD
# Tip Tracker
 
A Flask app for tracking server shifts and tips, and automatically allocating each pay period's earnings across checking, debt payoff, savings, and investments — based on a priority waterfall (checking buffer first, then debt, then a configurable percentage split) rather than a flat budget split.
 
Built as a personal project to solve a real problem: manually tracking tips and fund allocation in a spreadsheet every two weeks, and understanding relational database design well enough to model it properly instead of guessing.
 
## Features
 
- **Shift logging** — full CRUD (create, read, update, delete) for daily shifts: date, AM/PM, hours worked, cash tips, card tips
- **Custom pay-period math** — periods are calculated from a real anchor date in 14-day cycles, not calendar weeks/months, matching an actual biweekly pay schedule
- **Priority-based fund allocation** — on each period's "Calculate," earnings are allocated in order:
  1. Top up the checking account buffer
  2. Pay down debt (up to a configurable target — partial payment if earnings fall short)
  3. Split whatever's left across savings/investment destinations by configurable percentages
- **Immutable historical snapshots** — once a period is finalized, its numbers (total tips, buffer used, debt target vs. actual payment) are frozen permanently, even if settings change afterward
- **Editable account balances** — manually update real checking/debt/savings/stock balances between periods (no bank API integration — this is intentionally manual)
- **Authentication** — public read access (anyone can view the dashboard), but all write actions (logging shifts, editing balances, finalizing a period) require sign-in
## Tech Stack
 
- **Backend:** Flask, Flask-SQLAlchemy
- **Auth:** Flask-Login, Werkzeug password hashing
- **Database:** SQLite
- **Frontend:** Jinja2 templates, Tailwind CSS (via CDN)
- **Config:** python-dotenv
## Architecture
 
The app follows a layered structure to keep routing, business logic, and data separate:
 
```
api/         → Blueprints. Thin route handlers that decide GET vs POST
              and delegate to services. No business logic lives here.
services/    → The actual logic: form parsing, calculations, database writes.
models.py    → SQLAlchemy models and shared date-math helpers.
templates/   → Jinja2 templates, one per page/form.
```
 
## Data Model
 
| Model | Purpose |
|---|---|
| `Shift` | Daily tips + hours worked |
| `Destination` | Where money can go (checking, debt, savings, stock) — holds a live `current_balance` |
| `AllocationRule` | Current percentage split for savings/stock destinations |
| `Settings` | Live config: checking buffer target, debt payment target |
| `PayPeriod` | Frozen snapshot of a finalized period — total tips, settings used *at the time*, actual debt paid |
| `AllocationLog` | Per-destination breakdown of a finalized period's allocation |
| `User` | Single admin account for authentication |
 
`Settings` holds the *current* values; `PayPeriod` holds a *permanent copy* of whatever those values were at the moment a period was calculated — so changing your checking buffer target next month doesn't rewrite history for periods already finalized.
 
## Setup
 
```bash
# clone and enter the project
git clone <your-repo-url>
cd tip-tracker
 
# create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
 
# install dependencies
pip install -r requirements.txt
 
# set up your environment variables
cp .env.template .env
# then edit .env with your own values — see below
 
# run it
python app.py
```
 
Visit `http://localhost:5000`. The database and default seed data (destinations, settings, allocation rules, and your admin user) are created automatically on first run.
 
### Environment variables
 
See `.env.template` for the full list. You'll need:
- `ADMIN_USERNAME` / `ADMIN_PASSWORD` — your login credentials (only used once, to seed the initial `User` row)
- `SECRET_KEY` — generate one with `python -c "import secrets; print(secrets.token_hex(32))"`
- `COOKIE_DURATION` — how many days a login session stays valid
## Possible next steps
 
- Migrate from SQLite to PostgreSQL (e.g., AWS RDS) for real persistent hosting
- CSV export of shift/allocation history
- OIDC-based auth instead of a single hardcoded admin user, if this ever needs multiple users
 
