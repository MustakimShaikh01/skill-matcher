from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import uuid4


# ─── Resume Models ─────────────────────────────────────────────────────────────
class ResumeData(BaseModel):
    user_id: str = Field(default_factory=lambda: str(uuid4()))
    skills: List[str] = []
    experience: float = 0.0
    education: str = ""
    projects: List[str] = []
    raw_text: str = ""


class ResumeResponse(BaseModel):
    resume_id: str
    skills: List[str]
    experience: float
    education: str
    projects: List[str]
    message: str = "Resume parsed successfully"


# ─── Job Models ────────────────────────────────────────────────────────────────
class JobCreate(BaseModel):
    title: str
    description: str
    required_skills: List[str]


class JobResponse(BaseModel):
    job_id: str
    title: str
    description: str
    required_skills: List[str]


# ─── Match Models ──────────────────────────────────────────────────────────────
class MatchRequest(BaseModel):
    resume_id: str
    job_id: str


class RoadmapItem(BaseModel):
    week: int
    skill: str
    resources: List[str] = []
    description: str = ""


class MatchResponse(BaseModel):
    score: float
    grade: str
    missing_skills: List[str]
    matched_skills: List[str]
    roadmap: List[RoadmapItem]
    resume_id: str
    job_id: str


# ─── Skill Models ──────────────────────────────────────────────────────────────
class SkillNode(BaseModel):
    skill: str
    prerequisites: List[str] = []
    level: str = "beginner"  # beginner, intermediate, advanced
