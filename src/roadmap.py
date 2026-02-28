"""
Roadmap generator: compares user skills vs job requirements,
identifies gaps, and generates a structured learning plan.
"""
import re
from typing import Dict, List, Optional, Tuple
import numpy as np
from sentence_transformers.util import cos_sim

from src.recommender import get_model, get_cache
from src.config import SKILL_LEVEL_TIME, SKILL_NOISE_WORDS


# Curated skill → learning resources
SKILL_RESOURCES = {
    "python": ["Python.org docs", "Automate the Boring Stuff (free)", "CS50P (free)", "Stepik Python courses"],
    "sql": ["Mode SQL Tutorial (free)", "SQLZoo (free)", "pgExercises"],
    "excel": ["Excel Jet (free)", "Microsoft Learn"],
    "legal": ["Consultant.ru", "law school open courses", "Garant/Kodeks databases"],
    "law": ["Legal open courses", "Coursera Law specializations"],
    "english": ["italki", "Duolingo", "BBC Learning English (free)"],
    "data": ["Kaggle Learn (free)", "DataCamp", "Google Data Analytics cert"],
    "machine learning": ["fast.ai (free)", "Coursera ML Specialization", "Kaggle"],
    "java": ["Oracle Java tutorials", "Hyperskill", "Baeldung"],
    "javascript": ["javascript.info (free)", "freeCodeCamp", "MDN Web Docs"],
    "react": ["react.dev (official, free)", "Scrimba React course"],
    "marketing": ["Google Digital Garage (free)", "HubSpot Academy (free)"],
    "project management": ["PMI resources", "Google PM Certificate", "Coursera PM"],
    "communication": ["Toastmasters", "Coursera Communication courses"],
    "accounting": ["Stepik accounting courses", "1C training courses"],
    "photoshop": ["Adobe Learn (free)", "YouTube Adobe tutorials"],
    "figma": ["Figma Community (free)", "Coursera UX Design"],
    "statistics": ["Khan Academy Statistics (free)", "StatQuest YouTube"],
    "research": ["Research Methods textbooks", "Coursera Research courses"],
    "writing": ["Coursera Writing courses", "Purdue OWL (free)"],
    "default": ["Coursera", "Stepik", "YouTube tutorials", "Official documentation", "Practice projects"],
}


def _get_resources(skill_name: str) -> str:
    lower = skill_name.lower()
    for key, resources in SKILL_RESOURCES.items():
        if key in lower:
            return ", ".join(resources[:3])
    return ", ".join(SKILL_RESOURCES["default"])


def _detect_level(skill_text: str) -> str:
    """Detect required skill level from context words."""
    lower = skill_text.lower()
    if any(w in lower for w in ["expert", "эксперт", "глубокое", "proficient", "extensive"]):
        return "expert"
    if any(w in lower for w in ["advanced", "продвинутый", "senior", "strong knowledge"]):
        return "advanced"
    if any(w in lower for w in ["basic", "начальный", "beginner", "базовое", "introduction", "fundamentals"]):
        return "basic"
    if any(w in lower for w in ["foundational", "foundation", "основы", "elementary"]):
        return "foundational"
    return "intermediate"


def _is_noise_skill(text: str) -> bool:
    """Check if the skill text is a noise/soft-skill phrase."""
    lower = text.lower().strip()
    if lower in SKILL_NOISE_WORDS:
        return True
    # Also check if the text is a substring match of any noise word
    for noise in SKILL_NOISE_WORDS:
        if lower == noise or noise == lower:
            return True
    return False


def _extract_skills(text: str) -> List[str]:
    """
    Extract skill phrases from requirement/responsibility text.
    Splits on common delimiters and filters noise.
    """
    if not text:
        return []

    # normalize separators
    text = re.sub(r"[;\n•·]", ",", text)
    parts = [p.strip() for p in text.split(",")]

    skills = []
    for p in parts:
        # clean up
        p = re.sub(r"^\s*[-–—*]\s*", "", p).strip()
        p = re.sub(r"\s+", " ", p)

        # remove very short or very long fragments
        if len(p) < 3 or len(p) > 80:
            continue

        # skip pure number/date fragments
        if re.match(r"^[\d\s/\-–—\.]+$", p):
            continue

        # skip common filler phrases
        skip_patterns = [
            r"^(and|or|also|с|и|или|для|в|на|по|от|за)$",
            r"^(experience|опыт|знание|умение|навык)\s*$",
        ]
        if any(re.match(pat, p.lower()) for pat in skip_patterns):
            continue

        # Filter noise words (#10)
        if _is_noise_skill(p):
            continue

        skills.append(p)

    return skills


def _compute_user_skill_coverage(user_skills: List[str], job_skills: List[str]) -> List[Tuple[str, float]]:
    """
    For each job skill, find max similarity to any user skill.
    Uses batch encoding for efficiency (#11).
    Returns list of (skill, max_similarity) sorted by gap (lowest sim first).
    """
    model = get_model()
    cache = get_cache()

    if not user_skills:
        return [(s, 0.0) for s in job_skills]

    # Batch encode all at once
    all_texts = user_skills + job_skills
    all_embs = cache.encode(model, all_texts)
    user_embs = all_embs[:len(user_skills)]
    job_embs = all_embs[len(user_skills):]

    # Matrix cosine similarity: job_skills x user_skills
    sim_matrix = cos_sim(job_embs, user_embs)
    if hasattr(sim_matrix, 'cpu'):
        sim_matrix = sim_matrix.cpu().numpy()

    results = []
    for i, skill in enumerate(job_skills):
        max_sim = float(np.max(sim_matrix[i]))
        results.append((skill, max_sim))

    return results


def generate_roadmap(
    selected_job: Dict,
    user_skills_text: str,
    key_skills: Optional[List[str]] = None,
    skill_level: str = "intermediate",
) -> Dict:
    """
    Generate a personalized learning roadmap for the selected job.
    key_skills: structured skills from HH API /vacancies/{id} endpoint.
    skill_level: user's self-assessed level (beginner/intermediate/advanced).
    """
    # Combine requirement and responsibility for skill extraction
    req = (selected_job.get("requirement", "") + " " + selected_job.get("responsibility", "")).strip()

    job_skills = _extract_skills(req)

    # Prioritize key_skills from API if available (#14)
    if key_skills:
        # key_skills go first, then extracted skills that aren't already covered
        key_lower = {k.lower() for k in key_skills}
        extra = [s for s in job_skills if s.lower() not in key_lower]
        job_skills = key_skills + extra

    # Deduplicate and limit
    seen = set()
    unique_skills = []
    for s in job_skills:
        key = s.lower()
        if key not in seen:
            seen.add(key)
            unique_skills.append(s)
    job_skills = unique_skills[:20]

    user_skills = _extract_skills(user_skills_text)

    if not job_skills:
        return {
            "job_title": selected_job.get("name", ""),
            "missing_skills": [],
            "roadmap_steps": [],
            "total_estimated_time": "—",
            "match_after_preparation": "Unknown",
            "notes": "The vacancy description doesn't have enough detail to generate skill gaps.",
            "already_strong": [],
        }

    # Compute gaps
    skill_sims = _compute_user_skill_coverage(user_skills, job_skills)

    STRONG_THRESHOLD = 0.72    # user already has this
    PARTIAL_THRESHOLD = 0.48   # user partially has this

    missing_skills = []
    already_strong = []
    partial_skills = []

    for skill, sim in skill_sims:
        if sim >= STRONG_THRESHOLD:
            already_strong.append(skill)
        elif sim >= PARTIAL_THRESHOLD:
            partial_skills.append(skill)  # needs improvement
            missing_skills.append(skill)
        else:
            missing_skills.append(skill)

    # Adjust parallelism factor based on skill_level (#15)
    parallelism_map = {
        "beginner": 0.8,       # beginners learn more sequentially
        "intermediate": 0.65,  # default
        "advanced": 0.5,       # advanced learners can parallelize more
    }
    parallelism_factor = parallelism_map.get(skill_level, 0.65)

    # Build roadmap steps
    steps = []
    total_min_months = 0.0
    total_max_months = 0.0

    for skill, sim in skill_sims:
        if skill in already_strong:
            continue

        level = _detect_level(skill)
        # if partial, user needs less time → downgrade level
        if sim >= PARTIAL_THRESHOLD and level != "basic":
            downgrade = {"intermediate": "foundational", "advanced": "intermediate",
                         "expert": "advanced", "foundational": "basic"}
            level = downgrade.get(level, level)

        min_m, max_m = SKILL_LEVEL_TIME[level]
        total_min_months += min_m
        total_max_months += max_m

        status = "Improve" if sim >= PARTIAL_THRESHOLD else "Learn from scratch"
        resources = _get_resources(skill)

        steps.append({
            "skill": skill,
            "level": level,
            "status": status,
            "current_match_pct": round(sim * 100),
            "estimated_time": f"~{min_m}–{max_m} months",
            "min_months": min_m,
            "max_months": max_m,
            "suggested_actions": _get_action_advice(skill, status, level),
            "resources": resources,
        })

    # Sort by gap size (largest gap first)
    steps.sort(key=lambda x: x["current_match_pct"])

    # Estimated total time
    est_min = round(total_min_months * parallelism_factor, 1)
    est_max = round(total_max_months * parallelism_factor, 1)
    time_str = f"≈ {est_min}–{est_max} months (with parallel learning)"

    # Fix #12: realistic match_after based on actual similarity scores
    if skill_sims:
        current_avg_sim = sum(sim for _, sim in skill_sims) / len(skill_sims)
        # After preparation, assume gaps close to ~0.85 average
        projected_avg = 0.85
        # Blend: current strong skills stay, gaps improve
        strong_contribution = len(already_strong) * 0.90
        gap_contribution = len(missing_skills) * projected_avg
        total_skills = max(len(job_skills), 1)
        match_after = round((strong_contribution + gap_contribution) / total_skills * 100)
        match_after = min(match_after, 95)
        match_after = max(match_after, round(current_avg_sim * 100) + 5)
        match_after = min(match_after, 95)
    else:
        match_after = 70

    return {
        "job_title": selected_job.get("name", ""),
        "missing_skills": missing_skills,
        "already_strong": already_strong,
        "roadmap_steps": steps,
        "total_estimated_time": time_str,
        "match_after_preparation": f"{match_after}% (estimated after completing roadmap)",
        "notes": (
            "Time estimates assume ~10–15 hours/week of focused study. "
            "Skills can be learned in parallel. Real progress depends on your dedication and background."
        ),
    }


def _get_action_advice(skill: str, status: str, level: str) -> str:
    lower = skill.lower()

    if "law" in lower or "legal" in lower or "юрид" in lower or "право" in lower:
        return (
            "Study the specific legal domain through textbooks and open university lectures. "
            "Follow real case studies. Consider mock trials or pro bono volunteer work."
        )
    if "python" in lower or "programming" in lower or "код" in lower:
        return (
            "Build small projects (scripts, automation, bots). "
            "Solve daily coding challenges on LeetCode or Codewars. "
            "Contribute to open source projects."
        )
    if "excel" in lower or "spreadsheet" in lower:
        return (
            "Practice with real data sets. Learn pivot tables, VLOOKUP, and charts. "
            "Try building a mini dashboard with your own data."
        )
    if "english" in lower or "английский" in lower:
        return (
            "Immerse yourself: set your phone/apps to English. "
            "Practice speaking with native speakers on iTalki or HelloTalk. "
            "Read English business news daily."
        )
    if "communication" in lower or "communication" in lower:
        return (
            "Join a Toastmasters club or local debate group. "
            "Practice structured presentations. Seek feedback regularly."
        )
    if "research" in lower or "аналитика" in lower:
        return (
            "Work on a personal research project on a topic you're passionate about. "
            "Learn to find credible sources and synthesize information into clear reports."
        )

    if status == "Improve":
        return (
            f"You have a partial foundation in {skill}. "
            f"Focus on {level}-level materials, targeted practice, and real-world application. "
            "Review gaps by doing practical exercises or mini-projects."
        )
    return (
        f"Start with {level}-level introductory materials for {skill}. "
        "Follow a structured curriculum, then apply knowledge in a hands-on project. "
        "Join communities or forums to accelerate learning."
    )
