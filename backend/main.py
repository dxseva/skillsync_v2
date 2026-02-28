"""
SkillSync Pro v2 — FastAPI Backend
Exposes search, roadmap, and cities endpoints for the React frontend.
"""
import logging
import os
import sys
from typing import Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

# Ensure src/ is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.config import CITY_AREA_IDS
from src.fetcher import fetch_live_jobs, fetch_vacancy_details, HHApiError
from src.recommender import get_recommendations
from src.translator import translate_ru_to_en
from src.roadmap import generate_roadmap

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("skillsync")

app = FastAPI(title="SkillSync Pro API", version="2.0.0")

# CORS — allow configurable origins via env, fallback to dev defaults
_cors_origins = os.environ.get(
    "CORS_ORIGINS", "http://localhost:5173,http://localhost:3000"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in _cors_origins],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled error on %s %s", request.method, request.url.path)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error. Please try again."},
    )


# ── Request / Response models ───────────────────────────────────────────────

class ProfilePayload(BaseModel):
    skills: str = ""
    skill_level: str = Field(default="intermediate", pattern="^(beginner|intermediate|advanced)$")
    year: int = Field(default=3, ge=0, le=6)
    city: str = "Any city"
    format: str = Field(default="any", pattern="^(any|remote|office|hybrid)$")
    relocation: bool = False


class SearchRequest(BaseModel):
    goal: str = Field(..., min_length=2, max_length=300)
    profile: ProfilePayload


class JobPayload(BaseModel):
    id: str = ""
    name: str = ""
    url: str = ""
    employer: str = ""
    employer_en: Optional[str] = None
    area: str = ""
    requirement: str = ""
    responsibility: str = ""
    salary: Optional[dict] = None
    schedule: str = ""
    experience: str = ""
    match_score: float = 0
    snippet_en: Optional[str] = None


class RoadmapRequest(BaseModel):
    job: JobPayload
    user_skills: str = ""
    key_skills: Optional[list[str]] = None
    skill_level: str = Field(default="intermediate", pattern="^(beginner|intermediate|advanced)$")


# ── Endpoints ───────────────────────────────────────────────────────────────

@app.get("/api/cities")
def get_cities():
    """Return available cities for filtering."""
    return list(CITY_AREA_IDS.keys())


@app.post("/api/search")
def search_jobs(req: SearchRequest):
    """Fetch live jobs from HH.ru, rank semantically, translate snippets."""
    logger.info("Search request: goal=%r city=%s format=%s", req.goal, req.profile.city, req.profile.format)
    profile = req.profile.model_dump()

    try:
        raw_jobs = fetch_live_jobs(req.goal, profile)
    except HHApiError as e:
        logger.warning("HH.ru API error: %s", e)
        raise HTTPException(
            status_code=502,
            detail=f"Could not reach HH.ru: {e}. Check your internet connection or try again later.",
        )

    if not raw_jobs:
        return {
            "jobs": [],
            "message": "HH.ru returned 0 vacancies for your goal and filters. "
                       "Try broadening your goal (e.g. 'lawyer' instead of 'tax lawyer'), "
                       "removing the city filter, or changing work format to 'Any'.",
        }

    recs = get_recommendations(raw_jobs, req.goal, profile)

    if not recs:
        return {
            "jobs": [],
            "message": "Could not find strong matches. Try adjusting your filters or broadening your goal.",
        }

    for rec in recs:
        req_text = rec.get("requirement", "")
        resp_text = rec.get("responsibility", "")
        snippet_ru = (req_text + " " + resp_text).strip()
        rec["snippet_en"] = translate_ru_to_en(snippet_ru) if snippet_ru else ""

    logger.info("Search complete: %d results for goal=%r", len(recs), req.goal)
    return {"jobs": recs, "message": f"Found {len(recs)} matching vacancies."}


@app.post("/api/roadmap")
def build_roadmap(req: RoadmapRequest):
    """Generate a personalized skill gap roadmap for the selected job."""
    logger.info("Roadmap request: job=%r skill_level=%s", req.job.name, req.skill_level)
    job_dict = req.job.model_dump()

    key_skills = req.key_skills or []
    if not key_skills:
        try:
            details = fetch_vacancy_details(req.job.id)
            key_skills = details.get("key_skills", [])
        except Exception as e:
            logger.warning("Failed to fetch key_skills for %s: %s", req.job.id, e)

    try:
        roadmap = generate_roadmap(
            job_dict,
            req.user_skills,
            key_skills=key_skills if key_skills else None,
            skill_level=req.skill_level,
        )
    except Exception as e:
        logger.exception("Roadmap generation failed for job %s", req.job.id)
        raise HTTPException(status_code=500, detail=f"Roadmap generation failed: {e}")

    logger.info("Roadmap complete: %d steps for job=%r", len(roadmap.get("roadmap_steps", [])), req.job.name)
    return roadmap
