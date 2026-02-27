"""
Resume Parser Service
=====================
Extracts structured data from PDF / DOCX resumes using:
  - pdfplumber (PDF text extraction)
  - docx2txt (DOCX extraction)
  - spaCy NLP (NER + pattern matching)
  - Trie-based skill normalization
"""
import re
import io
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

# ── Conditional imports (graceful fallback for dev without heavy deps) ─────────
try:
    import pdfplumber
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    logger.warning("pdfplumber not installed — PDF parsing disabled")

try:
    import docx2txt
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False
    logger.warning("docx2txt not installed — DOCX parsing disabled")

try:
    import spacy
    try:
        nlp = spacy.load("en_core_web_sm")
        SPACY_AVAILABLE = True
    except OSError:
        nlp = None
        SPACY_AVAILABLE = False
        logger.warning("spaCy model not loaded — falling back to regex NLP")
except ImportError:
    nlp = None
    SPACY_AVAILABLE = False

from app.services.skill_trie import skill_trie, KNOWN_SKILLS


# ── Regex patterns ─────────────────────────────────────────────────────────────
EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")
PHONE_RE = re.compile(r"(\+?\d[\d\s\-]{7,}\d)")
EXPERIENCE_RE = re.compile(
    r"(\d+\.?\d*)\s*(?:\+)?\s*(?:years?|yrs?)\s*(?:of\s+)?(?:experience|exp)?",
    re.IGNORECASE,
)
EDUCATION_KEYWORDS = [
    "b.tech", "b.e", "btech", "b.sc", "bsc", "b.com", "bca", "mca",
    "m.tech", "mtech", "m.sc", "mba", "phd", "bachelor", "master",
    "diploma", "graduate", "undergraduate", "degree",
]

SECTION_HEADERS = {
    "skills":     re.compile(r"(?i)^(skills?|technical skills?|core competencies|technologies)"),
    "experience": re.compile(r"(?i)^(experience|work experience|employment|professional experience)"),
    "education":  re.compile(r"(?i)^(education|academic|qualification)"),
    "projects":   re.compile(r"(?i)^(projects?|personal projects?|academic projects?)"),
    "summary":    re.compile(r"(?i)^(summary|objective|profile|about)"),
}


class ResumeParser:
    """Main resume parsing engine."""

    def __init__(self):
        self._known_skills_lower = {s.lower(): s for s in KNOWN_SKILLS}

    # ── Public API ─────────────────────────────────────────────────────────────

    def parse_pdf(self, file_bytes: bytes) -> Dict[str, Any]:
        """Extract text from PDF bytes and parse."""
        text = self._extract_pdf_text(file_bytes)
        return self._parse_text(text)

    def parse_docx(self, file_bytes: bytes) -> Dict[str, Any]:
        """Extract text from DOCX bytes and parse."""
        text = self._extract_docx_text(file_bytes)
        return self._parse_text(text)

    def parse_text(self, raw_text: str) -> Dict[str, Any]:
        """Parse plain text resume."""
        return self._parse_text(raw_text)

    # ── Text Extraction ────────────────────────────────────────────────────────

    def _extract_pdf_text(self, file_bytes: bytes) -> str:
        if not PDF_AVAILABLE:
            raise RuntimeError("pdfplumber is not installed")
        try:
            with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
                pages = [page.extract_text() or "" for page in pdf.pages]
                return "\n".join(pages)
        except Exception as e:
            logger.error(f"PDF extraction failed: {e}")
            return ""

    def _extract_docx_text(self, file_bytes: bytes) -> str:
        if not DOCX_AVAILABLE:
            raise RuntimeError("docx2txt is not installed")
        try:
            # docx2txt works on file path; write to temp
            import tempfile, os
            with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as tmp:
                tmp.write(file_bytes)
                tmp_path = tmp.name
            text = docx2txt.process(tmp_path)
            os.unlink(tmp_path)
            return text or ""
        except Exception as e:
            logger.error(f"DOCX extraction failed: {e}")
            return ""

    # ── Main Parsing Pipeline ──────────────────────────────────────────────────

    def _parse_text(self, text: str) -> Dict[str, Any]:
        """Full NLP pipeline on extracted text."""
        if not text.strip():
            return {
                "skills": [], "experience": 0.0,
                "education": "", "projects": [], "raw_text": text,
            }

        sections = self._split_into_sections(text)

        skills    = self._extract_skills(text, sections)
        exp       = self._extract_experience(text, sections)
        education = self._extract_education(text, sections)
        projects  = self._extract_projects(sections)

        return {
            "skills":     skills,
            "experience": exp,
            "education":  education,
            "projects":   projects,
            "raw_text":   text,
        }

    # ── Section Splitting ──────────────────────────────────────────────────────

    def _split_into_sections(self, text: str) -> Dict[str, str]:
        """Heuristic: split resume by section headers."""
        lines = text.split("\n")
        sections: Dict[str, List[str]] = {k: [] for k in SECTION_HEADERS}
        sections["other"] = []
        current_section = "other"

        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue
            matched = False
            for section, pattern in SECTION_HEADERS.items():
                if pattern.match(stripped):
                    current_section = section
                    matched = True
                    break
            if not matched:
                sections[current_section].append(stripped)

        return {k: "\n".join(v) for k, v in sections.items()}

    # ── Skill Extraction ───────────────────────────────────────────────────────

    def _extract_skills(self, full_text: str, sections: Dict[str, str]) -> List[str]:
        """
        Multi-strategy skill extraction:
        1. Trie lookup against known skills
        2. spaCy NER (if available)
        3. Section-based keyword matching
        """
        found: set = set()

        # Strategy 1: Trie — scan every word/phrase in full text
        words_and_phrases = self._generate_ngrams(full_text, max_n=3)
        for phrase in words_and_phrases:
            normalized = phrase.lower().strip()
            if normalized in self._known_skills_lower:
                found.add(self._known_skills_lower[normalized])
            elif skill_trie.search(phrase):
                found.add(phrase)

        # Strategy 2: spaCy NER for org/product names that might be technologies
        if SPACY_AVAILABLE and nlp:
            doc = nlp(full_text[:100000])  # cap text for performance
            for ent in doc.ents:
                if ent.label_ in ("ORG", "PRODUCT"):
                    candidate = ent.text.strip()
                    if skill_trie.search(candidate):
                        found.add(candidate)

        # Strategy 3: Skills section direct extraction
        skills_text = sections.get("skills", "")
        if skills_text:
            # split by common delimiters
            raw = re.split(r"[,|•\n\t/]+", skills_text)
            for item in raw:
                item = item.strip()
                if 1 < len(item) < 40:
                    normalized = item.lower()
                    if normalized in self._known_skills_lower:
                        found.add(self._known_skills_lower[normalized])

        return sorted(found)

    # ── Experience Extraction ──────────────────────────────────────────────────

    def _extract_experience(self, full_text: str, sections: Dict[str, str]) -> float:
        """Extract years of experience as float."""
        search_text = sections.get("experience", "") + " " + full_text
        matches = EXPERIENCE_RE.findall(search_text)
        if matches:
            values = [float(m) for m in matches]
            return max(values)
        # Fallback: count job blocks in experience section
        exp_section = sections.get("experience", "")
        if exp_section:
            job_blocks = re.findall(r"\d{4}", exp_section)
            if len(job_blocks) >= 2:
                years = sorted(set(int(y) for y in job_blocks))
                return max(0.0, float(years[-1] - years[0]))
        return 0.0

    # ── Education Extraction ───────────────────────────────────────────────────

    def _extract_education(self, full_text: str, sections: Dict[str, str]) -> str:
        """Extract highest education qualification."""
        search_text = (sections.get("education", "") + " " + full_text).lower()
        for keyword in EDUCATION_KEYWORDS:
            if keyword in search_text:
                # find the surrounding sentence
                idx = search_text.find(keyword)
                snippet = full_text[max(0, idx - 20): idx + 60]
                # clean and return
                snippet = re.sub(r"\s+", " ", snippet).strip()
                return snippet[:80] if snippet else keyword.upper()
        return "Not specified"

    # ── Project Extraction ─────────────────────────────────────────────────────

    def _extract_projects(self, sections: Dict[str, str]) -> List[str]:
        """Extract project titles from projects section."""
        proj_text = sections.get("projects", "")
        if not proj_text:
            return []
        lines = [l.strip() for l in proj_text.split("\n") if l.strip()]
        projects = []
        for line in lines:
            # Project titles are usually short (< 60 chars) and don't start with "–"
            if 5 < len(line) < 80 and not line.startswith(("–", "-", "•", "·")):
                projects.append(line)
            if len(projects) >= 6:
                break
        return projects

    # ── Utility ───────────────────────────────────────────────────────────────

    def _generate_ngrams(self, text: str, max_n: int = 3) -> List[str]:
        """Generate word unigrams, bigrams, trigrams from text."""
        # clean text first
        text = re.sub(r"[^\w\s.#+/]", " ", text)
        words = text.split()
        results = []
        for n in range(1, max_n + 1):
            for i in range(len(words) - n + 1):
                phrase = " ".join(words[i: i + n])
                results.append(phrase)
        return results


# Global parser instance
resume_parser = ResumeParser()
