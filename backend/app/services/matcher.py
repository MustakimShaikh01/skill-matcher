"""
Resume–Job Matcher Service
============================
Uses TF-IDF vectorization + Cosine Similarity (ML core module).
Also does direct skill-set intersection for a hybrid score.
"""
import re
import math
import logging
from typing import List, Dict, Tuple, Set

logger = logging.getLogger(__name__)

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    logger.warning("scikit-learn not available — using fallback matcher")

from app.services.skill_trie import skill_trie


def _clean_text(text: str) -> str:
    """Lowercase, strip punctuation, collapse whitespace."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s+#\.]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _tfidf_cosine_score(text_a: str, text_b: str) -> float:
    """Compute TF-IDF cosine similarity between two texts (0–1)."""
    if not SKLEARN_AVAILABLE:
        return _jaccard_score(text_a, text_b)
    try:
        vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            max_features=5000,
            stop_words="english",
        )
        tfidf_matrix = vectorizer.fit_transform([text_a, text_b])
        score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        return float(score)
    except Exception as e:
        logger.error(f"TF-IDF error: {e}")
        return _jaccard_score(text_a, text_b)


def _jaccard_score(text_a: str, text_b: str) -> float:
    """Fallback: Jaccard similarity on word sets."""
    set_a = set(text_a.split())
    set_b = set(text_b.split())
    if not set_a or not set_b:
        return 0.0
    return len(set_a & set_b) / len(set_a | set_b)


def _skill_overlap_score(
    resume_skills: List[str], required_skills: List[str]
) -> Tuple[float, List[str], List[str]]:
    """
    Direct skill-set intersection.
    Returns (score 0–1, matched_skills, missing_skills).
    """
    if not required_skills:
        return 1.0, resume_skills, []

    resume_lower: Set[str] = {s.lower() for s in resume_skills}
    required_lower: Dict[str, str] = {s.lower(): s for s in required_skills}

    matched = [
        required_lower[r]
        for r in required_lower
        if r in resume_lower
    ]
    missing = [
        required_lower[r]
        for r in required_lower
        if r not in resume_lower
    ]

    score = len(matched) / len(required_skills) if required_skills else 0.0
    return score, matched, missing


def compute_match(
    resume_skills: List[str],
    resume_text: str,
    job_description: str,
    required_skills: List[str],
    resume_experience: float = 0.0,
) -> Dict:
    """
    Hybrid match scoring:
      - 50% direct skill overlap (interpretable, fair)
      - 40% TF-IDF cosine on full texts (semantic)
      - 10% experience bonus (capped)

    Returns:
      score        : 0–100
      grade        : A / B / C / D / F
      matched_skills
      missing_skills
    """
    # ── Skill overlap ──────────────────────────────────────────────────────────
    skill_score, matched, missing = _skill_overlap_score(
        resume_skills, required_skills
    )

    # ── TF-IDF semantic match ──────────────────────────────────────────────────
    resume_clean = _clean_text(resume_text)
    job_clean    = _clean_text(job_description)
    semantic_score = _tfidf_cosine_score(resume_clean, job_clean)

    # ── Experience bonus (0–10 pts, capped at reasonable max) ─────────────────
    exp_bonus = min(resume_experience * 2, 10.0) / 100.0   # max 0.10

    # ── Weighted final score ───────────────────────────────────────────────────
    final = (skill_score * 0.50) + (semantic_score * 0.40) + exp_bonus
    final = max(0.0, min(1.0, final))
    score_100 = round(final * 100, 1)

    # ── Grade ──────────────────────────────────────────────────────────────────
    if score_100 >= 80:
        grade = "A"
    elif score_100 >= 65:
        grade = "B"
    elif score_100 >= 50:
        grade = "C"
    elif score_100 >= 35:
        grade = "D"
    else:
        grade = "F"

    return {
        "score":          score_100,
        "grade":          grade,
        "matched_skills": matched,
        "missing_skills": missing,
        "skill_score":    round(skill_score * 100, 1),
        "semantic_score": round(semantic_score * 100, 1),
    }
