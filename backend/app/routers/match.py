import logging
from fastapi import APIRouter, HTTPException
from app.models.schemas import MatchRequest, MatchResponse, RoadmapItem
from app.services.matcher import compute_match
from app.services.skill_graph import skill_graph
from app.services.roadmap import generate_roadmap
from app.utils.store import store

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/match", tags=["Matching"])


@router.post("/", response_model=MatchResponse, summary="Match resume against a job and get skill gap analysis")
async def match_resume(req: MatchRequest):
    # ── Fetch data ─────────────────────────────────────────────────────────────
    resume = store.get_resume(req.resume_id)
    if not resume:
        raise HTTPException(status_code=404, detail=f"Resume '{req.resume_id}' not found.")

    job = store.get_job(req.job_id)
    if not job:
        raise HTTPException(status_code=404, detail=f"Job '{req.job_id}' not found.")

    resume_skills  = resume.get("skills", [])
    resume_text    = resume.get("raw_text", " ".join(resume_skills))
    resume_exp     = resume.get("experience", 0.0)
    required_skills = job.get("required_skills", [])
    job_description = job.get("description", " ".join(required_skills))

    # ── Compute match score ────────────────────────────────────────────────────
    match_result = compute_match(
        resume_skills=resume_skills,
        resume_text=resume_text,
        job_description=job_description,
        required_skills=required_skills,
        resume_experience=resume_exp,
    )

    matched_skills  = match_result["matched_skills"]
    missing_skills  = match_result["missing_skills"]

    # ── Graph-based prerequisite analysis ─────────────────────────────────────
    # Find additional prerequisites of missing skills that are also missing
    all_missing = skill_graph.get_missing_prerequisites(
        known_skills=set(resume_skills),
        target_skills=set(required_skills),
    )
    # Merge with direct missing (union)
    combined_missing = list(dict.fromkeys(missing_skills + [
        s for s in all_missing if s not in missing_skills
    ]))

    # ── Generate roadmap ───────────────────────────────────────────────────────
    roadmap_raw = generate_roadmap(
        missing_skills=combined_missing,
        known_skills=resume_skills,
    )
    roadmap = [RoadmapItem(**item) for item in roadmap_raw]

    # ── Store result ───────────────────────────────────────────────────────────
    result_data = {
        "resume_id":      req.resume_id,
        "job_id":         req.job_id,
        "score":          match_result["score"],
        "grade":          match_result["grade"],
        "matched_skills": matched_skills,
        "missing_skills": combined_missing,
        "roadmap":        [r.model_dump() for r in roadmap],
    }
    store.save_result(result_data)

    return MatchResponse(
        score=match_result["score"],
        grade=match_result["grade"],
        matched_skills=matched_skills,
        missing_skills=combined_missing,
        roadmap=roadmap,
        resume_id=req.resume_id,
        job_id=req.job_id,
    )


@router.post("/text", summary="Match using raw resume text and job description (no upload needed)")
async def match_text(resume_text: str, job_description: str, required_skills: list[str] = []):
    """Quick match without file upload — useful for testing."""
    from app.services.resume_parser import resume_parser
    parsed = resume_parser.parse_text(resume_text)
    result = compute_match(
        resume_skills=parsed["skills"],
        resume_text=resume_text,
        job_description=job_description,
        required_skills=required_skills,
    )
    all_missing = skill_graph.get_missing_prerequisites(
        known_skills=set(parsed["skills"]),
        target_skills=set(required_skills),
    )
    roadmap_raw = generate_roadmap(missing_skills=all_missing, known_skills=parsed["skills"])
    return {
        **result,
        "parsed_skills": parsed["skills"],
        "roadmap": roadmap_raw,
    }
