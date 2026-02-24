import re
import pdfplumber


def extract_text_from_pdf(pdf_path):
    """Extract all text from a PDF file using pdfplumber."""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()


def normalize_text(text):
    """Lowercase and collapse whitespace for matching."""
    text = text.lower()
    text = re.sub(r"[^\w\s/+#]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def match_keywords(cv_text, keywords):
    """Check which keywords from the job ad appear in the CV text.

    Returns (matched, missing) lists.
    """
    normalized_cv = normalize_text(cv_text)

    matched = []
    missing = []

    for keyword in keywords:
        normalized_kw = normalize_text(keyword)
        if normalized_kw in normalized_cv:
            matched.append(keyword)
        else:
            missing.append(keyword)

    return matched, missing


def compute_score(matched, total_keywords):
    """Score as a percentage of matched keywords."""
    if total_keywords == 0:
        return 0.0
    return round((len(matched) / total_keywords) * 100, 1)


def generate_suggestions(missing_keywords):
    """Generate simple tips based on missing keywords."""
    suggestions = []
    for kw in missing_keywords[:5]:
        suggestions.append(f'Consider adding experience with "{kw}" to your CV')
    if len(missing_keywords) > 5:
        suggestions.append(
            f"...and {len(missing_keywords) - 5} more keywords to consider"
        )
    return suggestions


def highlight_keywords_in_text(cv_text, matched_keywords):
    """Wrap matched keywords in <mark> tags for display."""
    highlighted = cv_text
    for keyword in sorted(matched_keywords, key=len, reverse=True):
        pattern = re.compile(re.escape(keyword), re.IGNORECASE)
        highlighted = pattern.sub(
            lambda m: f"<mark>{m.group()}</mark>", highlighted
        )
    return highlighted


def scan_cv(pdf_path, job_keywords):
    """Full pipeline: extract text, match keywords, compute score, generate suggestions."""
    cv_text = extract_text_from_pdf(pdf_path)
    matched, missing = match_keywords(cv_text, job_keywords)
    score = compute_score(matched, len(job_keywords))
    suggestions = generate_suggestions(missing)

    return {
        "cv_text": cv_text,
        "matched_keywords": matched,
        "missing_keywords": missing,
        "score": score,
        "suggestions": suggestions,
    }
