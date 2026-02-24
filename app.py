import json
import os
import shutil
import sqlite3
from functools import wraps

from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    send_from_directory,
    session,
    url_for,
)
from werkzeug.utils import secure_filename

from job_ads import get_job_ad, get_job_ads
from scanner import highlight_keywords_in_text, scan_cv

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = os.path.join(os.path.dirname(__file__), "uploads")
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # 5 MB limit
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")

ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "01071988")
DATABASE = os.path.join(os.path.dirname(__file__), "ats.db")


def parse_tiered_keywords(json_str):
    """Parse a JSON string that may be a flat list (old) or a tiered dict (new).

    Always returns {"must_have": [...], "nice_to_have": [...]}.
    """
    data = json.loads(json_str)
    if isinstance(data, list):
        return {"must_have": data, "nice_to_have": []}
    return data


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with open(os.path.join(os.path.dirname(__file__), "schema.sql")) as f:
        schema = f.read()
    conn = get_db()
    conn.executescript(schema)
    conn.close()


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("admin"):
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)
    return decorated


# --- Public Routes ---


@app.route("/")
def index():
    job_ads = get_job_ads()
    return render_template("index.html", job_ads=job_ads)


@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name", "").strip()
    job_id = request.form.get("job_id", "")
    pdf_file = request.files.get("pdf")

    if not name or not job_id or not pdf_file:
        flash("Please fill in all fields and upload a PDF.", "error")
        return redirect(url_for("index"))

    if not pdf_file.filename.lower().endswith(".pdf"):
        flash("Please upload a PDF file.", "error")
        return redirect(url_for("index"))

    job_ad = get_job_ad(job_id)
    if not job_ad:
        flash("Invalid job selection.", "error")
        return redirect(url_for("index"))

    # Save the PDF
    filename = secure_filename(pdf_file.filename)
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    # Add uniqueness to avoid overwrites
    base, ext = os.path.splitext(filename)
    import time
    unique_filename = f"{base}_{int(time.time())}{ext}"
    pdf_path = os.path.join(app.config["UPLOAD_FOLDER"], unique_filename)
    pdf_file.save(pdf_path)

    # Scan the CV
    try:
        result = scan_cv(pdf_path, job_ad["keywords"])
    except Exception as e:
        flash(f"Error processing PDF: {e}", "error")
        return redirect(url_for("index"))

    # Store in database (matched/missing stored as tiered dicts)
    conn = get_db()
    cursor = conn.execute(
        """INSERT INTO candidates (name, job_id, pdf_filename, cv_text, score,
           matched_keywords, missing_keywords, suggestions)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            name,
            job_id,
            unique_filename,
            result["cv_text"],
            result["score"],
            json.dumps(result["matched_keywords"]),
            json.dumps(result["missing_keywords"]),
            json.dumps(result["suggestions"]),
        ),
    )
    conn.commit()
    candidate_id = cursor.lastrowid
    conn.close()

    return redirect(url_for("results", candidate_id=candidate_id))


@app.route("/results/<int:candidate_id>")
def results(candidate_id):
    conn = get_db()
    candidate = conn.execute(
        "SELECT * FROM candidates WHERE id = ?", (candidate_id,)
    ).fetchone()
    conn.close()

    if not candidate:
        flash("Candidate not found.", "error")
        return redirect(url_for("index"))

    job_ad = get_job_ad(candidate["job_id"])
    matched = parse_tiered_keywords(candidate["matched_keywords"])
    missing = parse_tiered_keywords(candidate["missing_keywords"])

    return render_template(
        "results.html",
        candidate=candidate,
        job_ad=job_ad,
        matched=matched,
        missing=missing,
        suggestions=json.loads(candidate["suggestions"]),
    )


# --- Admin Routes ---


@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    if session.get("admin"):
        return redirect(url_for("admin_dashboard"))

    if request.method == "POST":
        password = request.form.get("password", "")
        if password == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect(url_for("admin_dashboard"))
        flash("Incorrect password.", "error")

    return render_template("admin_login.html")


@app.route("/admin/dashboard")
@admin_required
def admin_dashboard():
    job_filter = request.args.get("job", "all")
    conn = get_db()

    if job_filter != "all":
        candidates = conn.execute(
            "SELECT * FROM candidates WHERE job_id = ? ORDER BY score DESC",
            (job_filter,),
        ).fetchall()
    else:
        candidates = conn.execute(
            "SELECT * FROM candidates ORDER BY score DESC"
        ).fetchall()

    conn.close()
    job_ads = get_job_ads()
    return render_template(
        "admin_dashboard.html",
        candidates=candidates,
        job_ads=job_ads,
        current_filter=job_filter,
    )


@app.route("/admin/candidate/<int:candidate_id>")
@admin_required
def admin_candidate(candidate_id):
    conn = get_db()
    candidate = conn.execute(
        "SELECT * FROM candidates WHERE id = ?", (candidate_id,)
    ).fetchone()
    conn.close()

    if not candidate:
        flash("Candidate not found.", "error")
        return redirect(url_for("admin_dashboard"))

    job_ad = get_job_ad(candidate["job_id"])
    matched = parse_tiered_keywords(candidate["matched_keywords"])
    missing = parse_tiered_keywords(candidate["missing_keywords"])
    all_matched = matched["must_have"] + matched["nice_to_have"]
    highlighted_text = highlight_keywords_in_text(candidate["cv_text"], all_matched)

    return render_template(
        "admin_candidate.html",
        candidate=candidate,
        job_ad=job_ad,
        matched=matched,
        missing=missing,
        highlighted_text=highlighted_text,
    )


@app.route("/admin/pdf/<int:candidate_id>")
@admin_required
def admin_pdf(candidate_id):
    conn = get_db()
    candidate = conn.execute(
        "SELECT pdf_filename FROM candidates WHERE id = ?", (candidate_id,)
    ).fetchone()
    conn.close()

    if not candidate:
        flash("Candidate not found.", "error")
        return redirect(url_for("admin_dashboard"))

    return send_from_directory(app.config["UPLOAD_FOLDER"], candidate["pdf_filename"])


@app.route("/admin/delete-all", methods=["POST"])
@admin_required
def admin_delete_all():
    conn = get_db()
    conn.execute("DELETE FROM candidates")
    conn.commit()
    conn.close()

    # Clear uploads folder
    upload_dir = app.config["UPLOAD_FOLDER"]
    if os.path.exists(upload_dir):
        shutil.rmtree(upload_dir)
    os.makedirs(upload_dir, exist_ok=True)

    flash("All candidate data has been deleted.", "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/logout")
def admin_logout():
    session.pop("admin", None)
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    app.run(debug=True, port=5000)
