import logging
import os
from typing import Annotated
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from app.services.resume_parser import resume_parser
from app.services.skill_trie import skill_trie
from app.utils.store import store
from app.core.config import settings

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/resume", tags=["Resume"])

ALLOWED_TYPES = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "text/plain",
}
MAX_BYTES = settings.MAX_FILE_SIZE_MB * 1024 * 1024


@router.post("/upload", summary="Upload and parse a resume (PDF / DOCX / TXT)")
async def upload_resume(file: Annotated[UploadFile, File(description="Resume file (PDF/DOCX/TXT, max 2 MB)")]):
    # ── Validate file type ────────────────────────────────────────────────────
    content_type = file.content_type or ""
    filename     = file.filename or ""
    ext          = os.path.splitext(filename)[-1].lower()

    if content_type not in ALLOWED_TYPES and ext not in (".pdf", ".docx", ".txt"):
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Unsupported file type '{content_type}'. Upload PDF, DOCX, or TXT.",
        )

    # ── Read and size-check ───────────────────────────────────────────────────
    file_bytes = await file.read()
    if len(file_bytes) > MAX_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File exceeds {settings.MAX_FILE_SIZE_MB} MB limit.",
        )

    # ── Parse ─────────────────────────────────────────────────────────────────
    try:
        if ext == ".pdf" or "pdf" in content_type:
            parsed = resume_parser.parse_pdf(file_bytes)
        elif ext == ".docx" or "wordprocessingml" in content_type:
            parsed = resume_parser.parse_docx(file_bytes)
        else:
            parsed = resume_parser.parse_text(file_bytes.decode("utf-8", errors="ignore"))
    except RuntimeError as e:
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=str(e))
    except Exception as e:
        logger.exception("Parse error")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to parse resume.")

    # ── Normalise skills via Trie ─────────────────────────────────────────────
    parsed["skills"] = skill_trie.normalize_skills(parsed.get("skills", []))

    # ── Persist ───────────────────────────────────────────────────────────────
    resume_id = store.save_resume(parsed)

    return {
        "resume_id": resume_id,
        "skills":    parsed["skills"],
        "experience": parsed["experience"],
        "education":  parsed["education"],
        "projects":   parsed["projects"],
        "message":   "Resume parsed successfully",
    }


@router.get("/{resume_id}", summary="Get stored resume by ID")
async def get_resume(resume_id: str):
    resume = store.get_resume(resume_id)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found.")
    return resume


@router.get("/", summary="List all stored resumes")
async def list_resumes():
    return store.list_resumes()
