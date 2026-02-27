"""
In-Memory Store
===============
Thread-safe in-memory store used when MongoDB/PostgreSQL are unavailable.
Allows the app to run fully local without any database.
"""
import threading
from typing import Dict, Optional, List, Any
from uuid import uuid4
from datetime import datetime


class InMemoryStore:
    def __init__(self):
        self._lock = threading.Lock()
        self._resumes: Dict[str, Dict] = {}
        self._jobs: Dict[str, Dict] = {}
        self._results: Dict[str, Dict] = {}
        self._seed_jobs()

    def _seed_jobs(self):
        """Pre-populate with sample jobs for demo purposes."""
        sample_jobs = [
            {
                "job_id": "job-001",
                "title": "Full Stack Developer",
                "description": (
                    "We are looking for a Full Stack Developer proficient in React, Node.js, "
                    "and MongoDB. You will build scalable web applications, design RESTful APIs, "
                    "and work with cloud services like AWS. Experience with Docker and CI/CD is a plus. "
                    "Strong understanding of JavaScript, TypeScript, HTML, and CSS required."
                ),
                "required_skills": ["React", "Node.js", "MongoDB", "JavaScript", "TypeScript", "Docker", "REST API", "Git"],
                "created_at": datetime.utcnow().isoformat(),
            },
            {
                "job_id": "job-002",
                "title": "Machine Learning Engineer",
                "description": (
                    "Join our AI team to develop and deploy machine learning models. "
                    "Must have strong Python skills, experience with scikit-learn, TensorFlow or PyTorch. "
                    "You will work on NLP pipelines, model training, and production deployment. "
                    "Knowledge of Pandas, NumPy, and data visualisation is essential."
                ),
                "required_skills": ["Python", "Machine Learning", "TensorFlow", "scikit-learn", "NumPy", "Pandas", "NLP", "Deep Learning"],
                "created_at": datetime.utcnow().isoformat(),
            },
            {
                "job_id": "job-003",
                "title": "Backend Engineer (Python)",
                "description": (
                    "We need a Backend Engineer to build high-performance APIs using FastAPI or Django. "
                    "Experience with PostgreSQL, Redis, and Docker is required. "
                    "You should be comfortable with system design, microservices architecture, "
                    "and deploying on cloud platforms like AWS or GCP."
                ),
                "required_skills": ["Python", "FastAPI", "PostgreSQL", "Redis", "Docker", "System Design", "REST API", "AWS"],
                "created_at": datetime.utcnow().isoformat(),
            },
            {
                "job_id": "job-004",
                "title": "Frontend React Developer",
                "description": (
                    "Looking for a passionate Frontend Developer with expertise in React and Next.js. "
                    "You will build beautiful, responsive UIs using Tailwind CSS and manage state with Redux. "
                    "TypeScript proficiency is required. Experience with GraphQL and REST APIs is a plus."
                ),
                "required_skills": ["React", "Next.js", "TypeScript", "Tailwind CSS", "Redux", "JavaScript", "HTML", "CSS"],
                "created_at": datetime.utcnow().isoformat(),
            },
            {
                "job_id": "job-005",
                "title": "DevOps Engineer",
                "description": (
                    "We are seeking a DevOps Engineer to manage our cloud infrastructure. "
                    "Must have experience with Docker, Kubernetes, and CI/CD pipelines using GitHub Actions. "
                    "Strong Linux skills and knowledge of AWS or GCP cloud services required. "
                    "Experience with Terraform and monitoring tools is preferred."
                ),
                "required_skills": ["Docker", "Kubernetes", "AWS", "CI/CD", "Linux", "GitHub Actions", "Terraform", "Git"],
                "created_at": datetime.utcnow().isoformat(),
            },
            {
                "job_id": "job-006",
                "title": "Data Scientist",
                "description": (
                    "Data Scientist role focusing on statistical analysis, predictive modelling, "
                    "and data visualisation. Strong Python skills with Pandas, NumPy, Matplotlib. "
                    "Experience with machine learning algorithms and SQL databases is required. "
                    "Knowledge of deep learning frameworks is a plus."
                ),
                "required_skills": ["Python", "Pandas", "NumPy", "Matplotlib", "Machine Learning", "SQL", "scikit-learn", "Data Structures"],
                "created_at": datetime.utcnow().isoformat(),
            },
        ]
        for job in sample_jobs:
            self._jobs[job["job_id"]] = job

    # ── Resume CRUD ────────────────────────────────────────────────────────────
    def save_resume(self, data: Dict) -> str:
        with self._lock:
            resume_id = str(uuid4())
            data["resume_id"] = resume_id
            data["created_at"] = datetime.utcnow().isoformat()
            self._resumes[resume_id] = data
            return resume_id

    def get_resume(self, resume_id: str) -> Optional[Dict]:
        return self._resumes.get(resume_id)

    def list_resumes(self) -> List[Dict]:
        return list(self._resumes.values())

    # ── Job CRUD ───────────────────────────────────────────────────────────────
    def save_job(self, data: Dict) -> str:
        with self._lock:
            job_id = data.get("job_id", str(uuid4()))
            data["job_id"] = job_id
            data["created_at"] = datetime.utcnow().isoformat()
            self._jobs[job_id] = data
            return job_id

    def get_job(self, job_id: str) -> Optional[Dict]:
        return self._jobs.get(job_id)

    def list_jobs(self) -> List[Dict]:
        return list(self._jobs.values())

    # ── Result CRUD ────────────────────────────────────────────────────────────
    def save_result(self, data: Dict) -> str:
        with self._lock:
            result_id = str(uuid4())
            data["result_id"] = result_id
            data["created_at"] = datetime.utcnow().isoformat()
            self._results[result_id] = data
            return result_id

    def get_result(self, result_id: str) -> Optional[Dict]:
        return self._results.get(result_id)


# Global singleton
store = InMemoryStore()
