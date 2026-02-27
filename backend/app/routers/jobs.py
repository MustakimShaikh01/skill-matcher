import logging
from typing import List
from fastapi import APIRouter, HTTPException, status
from app.models.schemas import JobCreate, JobResponse
from app.utils.store import store

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.get("/", response_model=List[JobResponse], summary="List all available jobs")
async def list_jobs():
    return store.list_jobs()


@router.get("/{job_id}", response_model=JobResponse, summary="Get a specific job by ID")
async def get_job(job_id: str):
    job = store.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found.")
    return job


@router.post("/", response_model=JobResponse, status_code=status.HTTP_201_CREATED, summary="Create a new job posting")
async def create_job(job: JobCreate):
    data = job.model_dump()
    job_id = store.save_job(data)
    return {**data, "job_id": job_id}
