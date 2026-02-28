"""
Semantic recommender: scores jobs against English user query using a multilingual model.
The model (paraphrase-multilingual-mpnet-base-v2) natively handles English queries
matched against Russian job descriptions — no translation required.
"""
import numpy as np
from typing import List, Dict, Optional
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

from src.config import EMBEDDING_MODEL, DEFAULT_TOP_K
from src.embedding_cache import EmbeddingCache

_model: Optional[SentenceTransformer] = None
_cache: Optional[EmbeddingCache] = None


def get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBEDDING_MODEL)
    return _model


def get_cache() -> EmbeddingCache:
    global _cache
    if _cache is None:
        _cache = EmbeddingCache()
    return _cache


def _build_job_text(job: Dict) -> str:
    """Combine all job fields into one text for embedding (Russian is fine)."""
    parts = [
        job.get("name", ""),
        job.get("employer", ""),
        job.get("area", ""),
        job.get("schedule", ""),
        job.get("experience", ""),
        job.get("requirement", ""),
        job.get("responsibility", ""),
    ]
    return " | ".join(p for p in parts if p and p != "—")


def _build_user_query(goal: str, profile: Dict) -> str:
    """Enrich English user goal with profile context for better semantic matching."""
    year = profile.get("year", 0)
    status = "university student seeking entry-level or internship" if year > 0 else "recent graduate junior specialist"
    skills = profile.get("skills", "").strip()
    fmt = profile.get("format", "any")
    city = profile.get("city", "").strip()
    loc = f"in {city}" if city and city != "Any city" else ""

    return (
        f"{goal}. {status}. "
        f"Skills: {skills or 'general'}. "
        f"Work format: {fmt} {loc}. "
        "Junior entry-level position, internship, or trainee role."
    )


def get_recommendations(
    jobs: List[Dict],
    goal: str,
    profile: Dict,
    top_k: int = DEFAULT_TOP_K,
) -> List[Dict]:
    """
    Score jobs semantically against user's English goal.
    The multilingual model bridges English queries and Russian job text natively.
    Returns top_k jobs sorted by match score.
    """
    if not jobs:
        return []

    model = get_model()
    cache = get_cache()

    user_query = _build_user_query(goal, profile)
    job_texts = [_build_job_text(j) for j in jobs]

    # Use cache for batch encoding
    all_texts = [user_query] + job_texts
    all_embs = cache.encode(model, all_texts)

    user_emb = all_embs[0:1]
    job_embs = all_embs[1:]

    raw_scores = cos_sim(user_emb, job_embs)[0]
    if hasattr(raw_scores, 'cpu'):
        raw_scores = raw_scores.cpu().numpy()

    year = profile.get("year", 0)
    fmt = profile.get("format", "any").lower()

    adjusted = []
    for i, (job, score) in enumerate(zip(jobs, raw_scores)):
        s = float(score)
        name_lower = job.get("name", "").lower()
        sched = job.get("schedule", "").lower()

        if year > 0 and any(w in name_lower for w in ["senior", "lead", "head", "chief", "руководитель", "старший"]):
            s *= 0.6
        if "remote" in fmt and ("удалён" in sched or "remote" in sched):
            s *= 1.15
        s = min(s, 0.99)
        adjusted.append((i, s))

    adjusted.sort(key=lambda x: x[1], reverse=True)

    results = []
    seen_urls = set()
    for idx, score in adjusted:
        job = jobs[idx]
        url = job.get("url", "")
        if url in seen_urls:
            continue
        seen_urls.add(url)
        results.append({**job, "match_score": round(score * 100, 1)})
        if len(results) >= top_k:
            break

    return results
