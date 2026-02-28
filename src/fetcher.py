"""
Live HH.ru API fetcher — sends both English and Russian queries to maximize results.
Russian queries come from EN_TO_RU_QUERIES mapping. The multilingual embedding model
handles cross-lingual matching for scoring.
"""
import re
import time
import requests
from typing import List, Dict, Optional

from src.config import (
    HH_API_BASE, FETCH_PER_QUERY, MAX_PAGES_PER_QUERY,
    EN_TO_RU_QUERIES, CITY_AREA_IDS, HH_RUSSIA_AREA,
)

VACANCIES_URL = f"{HH_API_BASE}/vacancies"

HEADERS = {
    "User-Agent": "SkillSync/2.0",
    "Accept": "application/json",
}


def _clean_snippet(text: Optional[str]) -> str:
    if not text:
        return ""
    return re.sub(r"<[^>]+>", "", text).strip()


def _get_russian_queries(english_goal: str) -> List[str]:
    """Look up Russian search terms from EN_TO_RU_QUERIES for the given English goal."""
    goal_lower = english_goal.lower()
    ru_queries = []
    for key, values in EN_TO_RU_QUERIES.items():
        if key in goal_lower:
            ru_queries.extend(values)
    # Deduplicate preserving order
    seen = set()
    result = []
    for q in ru_queries:
        if q not in seen:
            seen.add(q)
            result.append(q)
    return result


def _build_queries(english_goal: str, profile: dict) -> List[str]:
    """
    Extract the core job role from free-text English input and build search queries.
    Combines English queries with Russian queries from EN_TO_RU_QUERIES.
    Handles inputs like 'Hey I want to become a Data Scientist' → ['data scientist', ...]
    """
    stop_words = {
        # filler / intent words
        "i", "want", "to", "be", "become", "a", "an", "the", "work", "as",
        "find", "get", "job", "in", "looking", "for", "interested", "into",
        "would", "like", "love", "hope", "wish", "my", "career", "hey", "hi",
        "hello", "please", "help", "me", "am", "is", "are", "was", "were",
        "will", "can", "could", "should", "need", "really", "very", "so",
        "maybe", "someday", "future", "dream", "goal", "plan", "trying",
        "study", "studying", "field", "area", "sector", "industry",
        # conjunctions / prepositions
        "and", "or", "but", "with", "about", "of", "on", "at", "by", "from",
        "that", "this", "it", "its", "do", "not", "no", "yes", "also",
        "people", "things", "something", "anything", "everything",
        # common but non-role words
        "new", "good", "great", "best", "top", "lead",
        "entry", "level", "position", "role", "opportunity", "graduate",
    }

    # clean and filter
    words = [w.strip(".,!?\"'()") for w in english_goal.lower().split()]
    role_words = [w for w in words if w and w not in stop_words and len(w) > 1]

    queries = []

    if role_words:
        # Primary: all role words joined (e.g. "data scientist", "machine learning engineer")
        queries.append(" ".join(role_words[:4]))

    if len(role_words) >= 2:
        # Secondary: first 2 words (e.g. "data scientist")
        queries.append(" ".join(role_words[:2]))

    if len(role_words) >= 1:
        # Tertiary: just the last/most specific word (e.g. "scientist", "lawyer")
        last = role_words[-1] if len(role_words) == 1 else role_words[1]
        if last not in [q.split()[-1] for q in queries]:
            queries.append(last)

    # Add junior variant for students
    year = profile.get("year", 0)
    if year > 0 and queries:
        queries.append(f"junior {queries[0]}")

    # Add Russian queries from EN_TO_RU_QUERIES (#4)
    ru_queries = _get_russian_queries(english_goal)
    queries.extend(ru_queries)

    # Deduplicate, preserve order, limit
    seen = set()
    result = []
    for q in queries:
        q = q.strip()
        if q and q not in seen:
            seen.add(q)
            result.append(q)

    print(f"[HH] Role words extracted: {role_words} → queries: {result[:8]}")
    return result[:8]


def _resolve_area(profile: dict) -> Optional[str]:
    """Resolve city + relocation into an HH.ru area parameter."""
    city = profile.get("city", "Any city")
    relocation = profile.get("relocation", False)

    if relocation or city == "Any city" or not city:
        return None  # search all of Russia (no area filter)

    area_id = CITY_AREA_IDS.get(city)
    return area_id


class HHApiError(Exception):
    """Raised when HH.ru API is unreachable or returns an unrecoverable error."""
    pass


def fetch_live_jobs(english_goal: str, profile: dict, max_total: int = 150) -> List[Dict]:
    """
    Fetch vacancies from HH.ru using English + Russian search queries.
    Returns raw job dicts (fields may be in Russian — matched via multilingual embeddings).
    Raises HHApiError on connection failures.
    """
    queries = _build_queries(english_goal, profile)
    print(f"[HH] Built queries from '{english_goal}': {queries}")

    fmt = profile.get("format", "any").lower()
    # Fix #8: hybrid has no direct HH schedule equivalent — don't filter
    schedule_map = {"remote": "remote", "office": "fullDay"}
    schedule_param = schedule_map.get(fmt)

    # Resolve area from city + relocation (#5, #6, #7)
    area_id = _resolve_area(profile)

    all_jobs: List[Dict] = []
    seen_ids: set = set()

    # Run each query with multiple experience levels to maximize results
    experience_levels = ["noExperience", "between1And3", "between3And6"]

    for query in queries:
        print(f"[HH] Searching: '{query}'")
        if len(all_jobs) >= max_total:
            break

        for experience in experience_levels:
            if len(all_jobs) >= max_total:
                break

            params: Dict = {
                "text": query,
                "per_page": FETCH_PER_QUERY,  # Fix #9: use config constant
                "experience": experience,
            }
            if schedule_param:
                params["schedule"] = schedule_param
            if area_id:
                params["area"] = area_id

            for page in range(MAX_PAGES_PER_QUERY):
                params["page"] = page
                try:
                    r = requests.get(VACANCIES_URL, params=params, headers=HEADERS, timeout=15)
                    r.raise_for_status()
                    data = r.json()
                    found = data.get("found", 0)
                    print(f"[HH] query='{query}' exp={experience} page={page} → {len(data.get('items', []))} items, found: {found}")
                except requests.exceptions.ConnectionError as e:
                    raise HHApiError(f"Cannot connect to HH.ru. Check your internet connection.\n\n{e}") from e
                except requests.exceptions.Timeout as e:
                    raise HHApiError(f"HH.ru timed out. Try again in a moment.\n\n{e}") from e
                except requests.exceptions.HTTPError as e:
                    status = e.response.status_code if e.response is not None else 0
                    if status == 400:
                        print(f"[HH] 400 for query='{query}' exp={experience}")
                        print(f"[HH] 400 body: {e.response.text[:400]}")
                        break
                    raise HHApiError(f"HH.ru returned HTTP {status}.\n\n{e}") from e
                except Exception as e:
                    print(f"[HH] Unexpected error for query='{query}': {e}")
                    break

                items = data.get("items", [])
                if not items:
                    break

                for v in items:
                    vid = v.get("id")
                    if vid in seen_ids:
                        continue
                    seen_ids.add(vid)

                    snippet = v.get("snippet", {})
                    all_jobs.append({
                        "id": vid,
                        "name": v.get("name", ""),
                        "url": v.get("alternate_url", ""),
                        "employer": (v.get("employer") or {}).get("name", "—"),
                        "area": (v.get("area") or {}).get("name", "—"),
                        "requirement": _clean_snippet(snippet.get("requirement")),
                        "responsibility": _clean_snippet(snippet.get("responsibility")),
                        "salary": v.get("salary"),
                        "schedule": (v.get("schedule") or {}).get("name", ""),
                        "experience": (v.get("experience") or {}).get("name", ""),
                    })

                time.sleep(0.3)

                if page >= data.get("pages", 1) - 1:
                    break

    print(f"[HH] Total collected: {len(all_jobs)} unique vacancies")
    return all_jobs


def fetch_vacancy_details(vacancy_id: str) -> Dict:
    """Fetch full vacancy details including key_skills from /vacancies/{id}."""
    url = f"{VACANCIES_URL}/{vacancy_id}"
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        r.raise_for_status()
        data = r.json()
        return {
            "key_skills": [s["name"] for s in data.get("key_skills", [])],
            "description": _clean_snippet(data.get("description", "")),
        }
    except Exception as e:
        print(f"[HH] Failed to fetch details for vacancy {vacancy_id}: {e}")
        return {"key_skills": [], "description": ""}


def fetch_key_skills_for_jobs(jobs: List[Dict], max_jobs: int = 6) -> Dict[str, List[str]]:
    """
    Fetch key_skills for multiple vacancies. Returns {vacancy_id: [skill1, skill2, ...]}.
    Rate-limited with delays between requests.
    """
    result = {}
    for job in jobs[:max_jobs]:
        vid = job.get("id")
        if not vid:
            continue
        details = fetch_vacancy_details(vid)
        result[vid] = details["key_skills"]
        time.sleep(0.3)
    return result
