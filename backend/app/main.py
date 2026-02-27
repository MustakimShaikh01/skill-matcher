"""
SkillMatch AI — FastAPI Application Entry Point
"""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from app.core.config import settings
from app.core.database import connect_mongodb, close_mongodb, connect_postgres, close_postgres
from app.routers import resume, jobs, match, skills

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s — %(message)s",
)
logger = logging.getLogger(__name__)


# ── Lifespan ───────────────────────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(" SkillMatch AI starting up…")
    await connect_mongodb()
    await connect_postgres()
    yield
    logger.info(" SkillMatch AI shutting down…")
    await close_mongodb()
    await close_postgres()


# ── App factory ────────────────────────────────────────────────────────────────
app = FastAPI(
    title="SkillMatch AI API",
    description=(
        "AI-driven resume–job matching platform using NLP (spaCy + TF-IDF) "
        "and DSA (Trie + Graph). Match resumes to jobs, detect skill gaps, "
        "and generate dependency-ordered learning roadmaps."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# ── Middleware ─────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=1000)

# ── Routers ────────────────────────────────────────────────────────────────────
app.include_router(resume.router, prefix="/api/v1")
app.include_router(jobs.router,   prefix="/api/v1")
app.include_router(match.router,  prefix="/api/v1")
app.include_router(skills.router, prefix="/api/v1")


# ── Health check ───────────────────────────────────────────────────────────────
@app.get("/", tags=["Health"])
async def root():
    return {
        "service": "SkillMatch AI",
        "status":  "running",
        "version": "1.0.0",
        "docs":    "/docs",
    }


@app.get("/health", tags=["Health"])
async def health():
    return {"status": "healthy", "env": settings.ENV}
