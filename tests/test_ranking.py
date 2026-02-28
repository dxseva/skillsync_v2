"""Tests for src/recommender.py — semantic ranking quality, penalties, boosts."""
import pytest
from src.recommender import get_recommendations


@pytest.fixture
def python_jobs():
    return [
        {
            "id": "1", "name": "Junior Python Developer", "url": "https://hh.ru/1",
            "employer": "TechCo", "area": "Москва",
            "requirement": "Python, Django, REST API, Git",
            "responsibility": "Backend development, write tests",
            "salary": None, "schedule": "Удалённая работа", "experience": "Нет опыта",
        },
        {
            "id": "2", "name": "Senior Lead Architect", "url": "https://hh.ru/2",
            "employer": "BigCorp", "area": "Москва",
            "requirement": "15+ years experience, system design, team leadership",
            "responsibility": "Lead architecture team, strategic decisions",
            "salary": None, "schedule": "Полный день", "experience": "Более 6 лет",
        },
        {
            "id": "3", "name": "Python Data Analyst", "url": "https://hh.ru/3",
            "employer": "DataCo", "area": "Москва",
            "requirement": "Python, pandas, SQL, statistics, data visualization",
            "responsibility": "Analyze data, build dashboards",
            "salary": None, "schedule": "Удалённая работа", "experience": "От 1 до 3 лет",
        },
    ]


class TestSemanticRanking:
    def test_relevant_jobs_rank_higher(self, python_jobs):
        profile = {"skills": "Python, Django", "year": 3, "format": "any"}
        recs = get_recommendations(python_jobs, "python developer", profile, top_k=3)
        assert len(recs) > 0
        # Python developer should rank above senior architect for a student
        names = [r["name"] for r in recs]
        python_idx = next(i for i, n in enumerate(names) if "Python" in n)
        senior_idx = next(i for i, n in enumerate(names) if "Senior" in n)
        assert python_idx < senior_idx

    def test_senior_penalty_for_students(self, python_jobs):
        profile = {"skills": "Python basics", "year": 2, "format": "any"}
        recs = get_recommendations(python_jobs, "python developer", profile, top_k=3)
        # Senior should be demoted for year-2 student
        senior = next(r for r in recs if "Senior" in r["name"])
        junior = next(r for r in recs if "Junior" in r["name"])
        assert junior["match_score"] > senior["match_score"]

    def test_no_senior_penalty_for_graduates(self, python_jobs):
        profile = {"skills": "Python, 5 years experience", "year": 0, "format": "any"}
        recs = get_recommendations(python_jobs, "python developer", profile, top_k=3)
        # No penalty — scores not artificially reduced
        assert all(r["match_score"] > 0 for r in recs)

    def test_score_ranges(self, python_jobs):
        profile = {"skills": "Python", "year": 3, "format": "any"}
        recs = get_recommendations(python_jobs, "python developer", profile, top_k=3)
        for r in recs:
            assert 0 <= r["match_score"] <= 99

    def test_empty_jobs_returns_empty(self):
        recs = get_recommendations([], "developer", {"skills": "", "year": 0}, top_k=3)
        assert recs == []

    def test_remote_boost(self, python_jobs):
        profile_remote = {"skills": "Python", "year": 3, "format": "remote"}
        profile_any = {"skills": "Python", "year": 3, "format": "any"}
        recs_remote = get_recommendations(python_jobs, "python developer", profile_remote, top_k=3)
        recs_any = get_recommendations(python_jobs, "python developer", profile_any, top_k=3)
        # Remote job should score relatively higher when format is remote
        remote_job_remote = next(r for r in recs_remote if "Удалённая" in r.get("schedule", ""))
        remote_job_any = next(r for r in recs_any if r["id"] == remote_job_remote["id"])
        assert remote_job_remote["match_score"] >= remote_job_any["match_score"]
