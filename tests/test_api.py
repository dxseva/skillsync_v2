"""
Tests for the FastAPI backend endpoints.
Uses TestClient to test /api/cities, /api/search, /api/roadmap.
Mocks external calls (HH.ru API, ML models, translation) for speed and isolation.
"""
import sys
import os
from unittest.mock import patch, MagicMock

import pytest

# Ensure backend is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():
    return TestClient(app)


# ── GET /api/cities ────────────────────────────────────────────────────────


class TestGetCities:
    def test_returns_list(self, client):
        resp = client.get("/api/cities")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        assert len(data) > 0

    def test_contains_any_city(self, client):
        resp = client.get("/api/cities")
        cities = resp.json()
        assert "Any city" in cities

    def test_contains_known_cities(self, client):
        resp = client.get("/api/cities")
        cities = resp.json()
        # At least some well-known cities should be present
        assert any("Москва" in c for c in cities)


# ── POST /api/search ──────────────────────────────────────────────────────


class TestSearchJobs:
    def test_validation_rejects_empty_goal(self, client):
        resp = client.post("/api/search", json={
            "goal": "",
            "profile": {"skills": "Python", "skill_level": "intermediate", "year": 3,
                         "city": "Any city", "format": "any", "relocation": False},
        })
        assert resp.status_code == 422

    def test_validation_rejects_invalid_skill_level(self, client):
        resp = client.post("/api/search", json={
            "goal": "data analyst",
            "profile": {"skills": "Python", "skill_level": "expert", "year": 3,
                         "city": "Any city", "format": "any", "relocation": False},
        })
        assert resp.status_code == 422

    def test_validation_rejects_invalid_format(self, client):
        resp = client.post("/api/search", json={
            "goal": "data analyst",
            "profile": {"skills": "Python", "skill_level": "intermediate", "year": 3,
                         "city": "Any city", "format": "invalid_format", "relocation": False},
        })
        assert resp.status_code == 422

    def test_validation_rejects_year_out_of_range(self, client):
        resp = client.post("/api/search", json={
            "goal": "data analyst",
            "profile": {"skills": "Python", "skill_level": "intermediate", "year": 10,
                         "city": "Any city", "format": "any", "relocation": False},
        })
        assert resp.status_code == 422

    @patch("main.fetch_live_jobs")
    @patch("main.get_recommendations")
    @patch("main.translate_ru_to_en", side_effect=lambda t: f"[EN] {t}")
    def test_search_returns_jobs_with_translation(self, mock_translate, mock_recs, mock_fetch, client):
        mock_fetch.return_value = [
            {"id": "1", "name": "Dev", "employer": "Компания", "url": "https://hh.ru/1",
             "area": "Москва", "requirement": "Python", "responsibility": "Разработка",
             "salary": None, "schedule": "", "experience": "", "match_score": 85},
        ]
        mock_recs.return_value = mock_fetch.return_value

        resp = client.post("/api/search", json={
            "goal": "developer",
            "profile": {"skills": "Python", "skill_level": "intermediate", "year": 3,
                         "city": "Any city", "format": "any", "relocation": False},
        })

        assert resp.status_code == 200
        data = resp.json()
        assert "jobs" in data
        assert len(data["jobs"]) == 1
        assert data["jobs"][0]["snippet_en"] == "[EN] Python Разработка"
        assert data["jobs"][0]["employer_en"] == "[EN] Компания"

    @patch("main.fetch_live_jobs", return_value=[])
    def test_search_returns_empty_with_message(self, mock_fetch, client):
        resp = client.post("/api/search", json={
            "goal": "xyznonexistent",
            "profile": {"skills": "", "skill_level": "beginner", "year": 1,
                         "city": "Any city", "format": "any", "relocation": False},
        })

        assert resp.status_code == 200
        data = resp.json()
        assert data["jobs"] == []
        assert "message" in data
        assert len(data["message"]) > 0

    @patch("main.fetch_live_jobs", side_effect=__import__("src.fetcher", fromlist=["HHApiError"]).HHApiError("Connection timeout"))
    def test_search_hh_api_error_returns_502(self, mock_fetch, client):
        resp = client.post("/api/search", json={
            "goal": "developer",
            "profile": {"skills": "", "skill_level": "intermediate", "year": 3,
                         "city": "Any city", "format": "any", "relocation": False},
        })

        assert resp.status_code == 502
        assert "HH.ru" in resp.json()["detail"]

    @patch("main.fetch_live_jobs")
    @patch("main.get_recommendations")
    @patch("main.translate_ru_to_en", side_effect=RuntimeError("Model failed"))
    def test_search_translation_failure_graceful(self, mock_translate, mock_recs, mock_fetch, client):
        """Translation failure should not crash the endpoint — jobs returned without translation."""
        mock_fetch.return_value = [
            {"id": "1", "name": "Dev", "employer": "Corp", "url": "",
             "area": "", "requirement": "Req", "responsibility": "Resp",
             "salary": None, "schedule": "", "experience": "", "match_score": 90},
        ]
        mock_recs.return_value = mock_fetch.return_value

        resp = client.post("/api/search", json={
            "goal": "developer",
            "profile": {"skills": "Python", "skill_level": "intermediate", "year": 3,
                         "city": "Any city", "format": "any", "relocation": False},
        })

        assert resp.status_code == 200
        data = resp.json()
        assert len(data["jobs"]) == 1
        # Translation failed, should have empty fallback
        assert data["jobs"][0]["snippet_en"] == ""
        assert data["jobs"][0]["employer_en"] == ""


# ── POST /api/roadmap ─────────────────────────────────────────────────────


class TestBuildRoadmap:
    def test_validation_rejects_invalid_skill_level(self, client):
        resp = client.post("/api/roadmap", json={
            "job": {"id": "1", "name": "Dev"},
            "user_skills": "Python",
            "skill_level": "master",
        })
        assert resp.status_code == 422

    @patch("main.fetch_vacancy_details", return_value={"key_skills": [{"name": "Python"}]})
    @patch("main.generate_roadmap")
    def test_roadmap_returns_structure(self, mock_roadmap, mock_details, client):
        mock_roadmap.return_value = {
            "job_title": "Developer",
            "missing_skills": ["Docker"],
            "already_strong": ["Python"],
            "roadmap_steps": [
                {"skill": "Docker", "level": "Beginner", "status": "Learn from scratch",
                 "current_match_pct": 10, "estimated_time": "2-3 months",
                 "suggested_actions": "Take Docker course", "resources": "docker.com"},
            ],
            "total_estimated_time": "2-3 months",
            "match_after_preparation": "92%",
            "notes": "Focus on Docker first.",
        }

        resp = client.post("/api/roadmap", json={
            "job": {"id": "1", "name": "Developer", "url": "", "employer": "",
                    "area": "", "requirement": "Python, Docker", "responsibility": "",
                    "match_score": 75},
            "user_skills": "Python",
            "skill_level": "intermediate",
        })

        assert resp.status_code == 200
        data = resp.json()
        assert data["job_title"] == "Developer"
        assert "Python" in data["already_strong"]
        assert len(data["roadmap_steps"]) == 1
        assert data["roadmap_steps"][0]["skill"] == "Docker"

    @patch("main.fetch_vacancy_details", side_effect=Exception("Network error"))
    @patch("main.generate_roadmap")
    def test_roadmap_continues_when_key_skills_fetch_fails(self, mock_roadmap, mock_details, client):
        """If fetching key_skills fails, roadmap should still generate without them."""
        mock_roadmap.return_value = {
            "job_title": "Dev",
            "missing_skills": [],
            "already_strong": [],
            "roadmap_steps": [],
            "total_estimated_time": "0 months",
            "match_after_preparation": "100%",
            "notes": "Strong candidate.",
        }

        resp = client.post("/api/roadmap", json={
            "job": {"id": "99", "name": "Dev"},
            "user_skills": "Python",
            "skill_level": "beginner",
        })

        assert resp.status_code == 200
        # generate_roadmap should be called with empty key_skills
        mock_roadmap.assert_called_once()

    @patch("main.fetch_vacancy_details", return_value={"key_skills": []})
    @patch("main.generate_roadmap", side_effect=RuntimeError("Model crashed"))
    def test_roadmap_generation_failure_returns_500(self, mock_roadmap, mock_details, client):
        resp = client.post("/api/roadmap", json={
            "job": {"id": "1", "name": "Dev"},
            "user_skills": "Python",
            "skill_level": "intermediate",
        })

        assert resp.status_code == 500
        assert "Roadmap generation failed" in resp.json()["detail"]

    @patch("main.fetch_vacancy_details", return_value={"key_skills": []})
    @patch("main.generate_roadmap")
    def test_roadmap_with_provided_key_skills(self, mock_roadmap, mock_details, client):
        """When key_skills are provided in request, should not fetch from API."""
        mock_roadmap.return_value = {
            "job_title": "Dev",
            "missing_skills": [],
            "already_strong": ["Python"],
            "roadmap_steps": [],
            "total_estimated_time": "0",
            "match_after_preparation": "95%",
            "notes": "",
        }

        resp = client.post("/api/roadmap", json={
            "job": {"id": "1", "name": "Dev"},
            "user_skills": "Python",
            "key_skills": ["Python", "Docker"],
            "skill_level": "advanced",
        })

        assert resp.status_code == 200
        # fetch_vacancy_details should NOT be called since key_skills were provided
        mock_details.assert_not_called()
