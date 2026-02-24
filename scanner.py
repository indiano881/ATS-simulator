import re
import pdfplumber

MUST_HAVE_WEIGHT = 3
NICE_TO_HAVE_WEIGHT = 1


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


def compute_tiered_score(matched_must, total_must, matched_nice, total_nice):
    """Weighted score: must-have keywords worth 3 pts, nice-to-have worth 1 pt."""
    earned = len(matched_must) * MUST_HAVE_WEIGHT + len(matched_nice) * NICE_TO_HAVE_WEIGHT
    maximum = total_must * MUST_HAVE_WEIGHT + total_nice * NICE_TO_HAVE_WEIGHT
    if maximum == 0:
        return 0.0
    return round((earned / maximum) * 100, 1)


def generate_suggestions(missing_must_have, missing_nice_to_have):
    """Generate simple tips based on missing keywords, prioritizing must-have."""
    suggestions = []
    for kw in missing_must_have[:5]:
        suggestions.append(f'Consider adding experience with "{kw}" to your CV (must-have)')
    remaining = 5 - len(missing_must_have[:5])
    if remaining > 0:
        for kw in missing_nice_to_have[:remaining]:
            suggestions.append(f'Consider adding experience with "{kw}" to your CV')
    total_remaining = (
        max(0, len(missing_must_have) - 5) + max(0, len(missing_nice_to_have) - remaining)
    )
    if total_remaining > 0:
        suggestions.append(f"...and {total_remaining} more keywords to consider")
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
    """Full pipeline: extract text, match keywords, compute score, generate suggestions.

    job_keywords can be either:
    - A dict with "must_have" and "nice_to_have" lists (new tiered format)
    - A flat list of strings (old format — all treated as must-have)
    """
    cv_text = extract_text_from_pdf(pdf_path)

    # Support both tiered dict and flat list formats
    if isinstance(job_keywords, dict):
        must_have = job_keywords.get("must_have", [])
        nice_to_have = job_keywords.get("nice_to_have", [])
    else:
        must_have = list(job_keywords)
        nice_to_have = []

    matched_must, missing_must = match_keywords(cv_text, must_have)
    matched_nice, missing_nice = match_keywords(cv_text, nice_to_have)

    score = compute_tiered_score(
        matched_must, len(must_have), matched_nice, len(nice_to_have)
    )
    suggestions = generate_suggestions(missing_must, missing_nice)

    return {
        "cv_text": cv_text,
        "matched_keywords": {"must_have": matched_must, "nice_to_have": matched_nice},
        "missing_keywords": {"must_have": missing_must, "nice_to_have": missing_nice},
        "score": score,
        "suggestions": suggestions,
    }
