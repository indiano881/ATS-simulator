# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

Educational ATS-like CV scanner for a 1-hour workshop. **Not a real recruitment system.**

## Commands

- **Run:** `python app.py` (serves at http://localhost:5000, auto-creates `ats.db`)
- **Install deps:** `pip install -r requirements.txt`
- No test suite or linter is configured.

## Architecture

Single-process Flask app with SQLite. Three Python modules, six Jinja2 templates, one CSS file.

**Data flow:** Upload PDF → `scanner.scan_cv()` extracts text via pdfplumber, does substring keyword matching, computes score as percentage of matched keywords → result stored in SQLite `candidates` table → redirect to results page.

**Key design decisions:**
- Job ads are hardcoded in `job_ads.py` (not in the database): Embark Studios Fullstack Engineer + SS&C Eze Project Manager. To add a new job, add an entry to the `JOB_ADS` dict with an `id`, `title`, `company`, `description`, and `keywords` list.
- `candidates` table stores `matched_keywords`, `missing_keywords`, and `suggestions` as JSON-serialized TEXT columns. Always use `json.dumps()`/`json.loads()` when reading/writing these fields.
- All routes live in `app.py`. Admin routes are protected by the `@admin_required` decorator (session-based auth).
- Templates extend `base.html`. Admin templates are prefixed `admin_*.html`.
- PDFs are saved to `uploads/` with a unix-timestamp suffix for uniqueness.

## Environment Variables

- `ADMIN_PASSWORD` — Admin panel password (default: `workshop2024`)
- `SECRET_KEY` — Flask session secret (default: `dev-secret-key-change-me`)
