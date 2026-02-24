# ATS Scanner — Workshop Demo

Educational ATS-like CV scanner for a 1-hour workshop. **Not a real recruitment system.**

## Quick Start

```bash
pip install -r requirements.txt
python app.py
# Open http://localhost:5000
```

## Tech Stack

- Python 3 + Flask + Jinja2 templates + vanilla CSS
- SQLite (via `sqlite3`) — database file: `ats.db`
- `pdfplumber` for PDF text extraction
- TF-IDF-style keyword matching (no AI/LLM)

## Project Structure

- `app.py` — Flask app with all routes (public + admin)
- `scanner.py` — PDF extraction + keyword matching logic
- `job_ads.py` — Predefined job ad data (Frontend Dev + Marketing Coordinator)
- `schema.sql` — SQLite table definition
- `templates/` — Jinja2 templates (base, index, results, admin_*)
- `static/style.css` — Single stylesheet
- `uploads/` — Stored PDF files (gitignored)

## Key Routes

- `GET /` — Upload form (name + PDF + job selector)
- `POST /submit` — Process CV, store result, redirect to results
- `GET /results/<id>` — Score breakdown for a candidate
- `GET/POST /admin` — Admin login (password: env `ADMIN_PASSWORD`, default `workshop2024`)
- `GET /admin/dashboard` — Ranked candidates table
- `GET /admin/candidate/<id>` — Candidate detail with highlighted CV text

## How Matching Works

1. Extract text from PDF via `pdfplumber`
2. Normalize text (lowercase, strip punctuation)
3. Check which curated job keywords appear in CV text (substring match)
4. Score = (matched / total) * 100
5. Generate suggestions for missing keywords

## Environment Variables

- `ADMIN_PASSWORD` — Admin panel password (default: `workshop2024`)
- `SECRET_KEY` — Flask session secret (default: `dev-secret-key-change-me`)

## Commands

- Run: `python app.py`
- Install deps: `pip install -r requirements.txt`
