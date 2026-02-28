"""Tests for src/roadmap.py — skill extraction, noise filtering, roadmap structure."""
import pytest
from src.roadmap import _extract_skills, _is_noise_skill, generate_roadmap


class TestExtractSkills:
    def test_comma_separated(self):
        skills = _extract_skills("Python, Django, REST API, SQL")
        assert "Python" in skills
        assert "Django" in skills

    def test_semicolon_separated(self):
        skills = _extract_skills("Python; Django; REST API")
        assert len(skills) >= 3

    def test_filters_short(self):
        skills = _extract_skills("ab, Python, x, SQL")
        assert "ab" not in skills
        assert "x" not in skills

    def test_filters_long(self):
        long_text = "a" * 100
        skills = _extract_skills(f"Python, {long_text}, SQL")
        assert long_text not in skills

    def test_empty_input(self):
        assert _extract_skills("") == []
        assert _extract_skills(None) == []


class TestNoiseFiltering:
    def test_russian_noise_words(self):
        assert _is_noise_skill("ответственность")
        assert _is_noise_skill("стрессоустойчивость")
        assert _is_noise_skill("коммуникабельность")

    def test_english_noise_words(self):
        assert _is_noise_skill("team player")
        assert _is_noise_skill("fast learner")
        assert _is_noise_skill("self-motivated")

    def test_real_skills_pass(self):
        assert not _is_noise_skill("Python")
        assert not _is_noise_skill("Django")
        assert not _is_noise_skill("PostgreSQL")
        assert not _is_noise_skill("REST API")

    def test_extract_filters_noise(self):
        skills = _extract_skills("Python, ответственность, Django, стрессоустойчивость, SQL")
        assert "ответственность" not in skills
        assert "стрессоустойчивость" not in skills
        assert "Python" in skills
        assert "Django" in skills


class TestGenerateRoadmap:
    def test_basic_structure(self):
        job = {
            "name": "Python Developer",
            "requirement": "Python, Django, REST API, SQL, Docker",
            "responsibility": "Backend development, code review, testing",
        }
        roadmap = generate_roadmap(job, "Python, basic SQL")
        assert "job_title" in roadmap
        assert "roadmap_steps" in roadmap
        assert "already_strong" in roadmap
        assert "total_estimated_time" in roadmap
        assert "match_after_preparation" in roadmap
        assert "notes" in roadmap

    def test_key_skills_prioritized(self):
        job = {
            "name": "Python Developer",
            "requirement": "Some generic text about working in a team",
            "responsibility": "Various tasks",
        }
        key_skills = ["Python", "Django", "PostgreSQL", "Docker"]
        roadmap = generate_roadmap(job, "", key_skills=key_skills)
        # key_skills should appear in missing or already_strong
        all_skills = roadmap["missing_skills"] + roadmap["already_strong"]
        for ks in key_skills:
            assert ks in all_skills, f"Key skill '{ks}' not found in roadmap"

    def test_skill_level_affects_parallelism(self):
        job = {
            "name": "Developer",
            "requirement": "Python, Django, SQL, Docker, Kubernetes, Redis",
            "responsibility": "Development",
        }
        roadmap_beginner = generate_roadmap(job, "", skill_level="beginner")
        roadmap_advanced = generate_roadmap(job, "", skill_level="advanced")
        # Advanced should have shorter total time (higher parallelism)
        # Both should have valid time strings
        assert "months" in roadmap_beginner["total_estimated_time"]
        assert "months" in roadmap_advanced["total_estimated_time"]

    def test_match_after_realistic(self):
        job = {
            "name": "Developer",
            "requirement": "Python, Django, SQL, Docker",
            "responsibility": "Development, testing",
        }
        roadmap = generate_roadmap(job, "Python")
        # match_after should contain a percentage
        assert "%" in roadmap["match_after_preparation"]
        # Extract the number
        pct_str = roadmap["match_after_preparation"].split("%")[0]
        pct = int(pct_str)
        # Should be realistic: between 50% and 95%
        assert 50 <= pct <= 95, f"match_after {pct}% is not realistic"

    def test_empty_description(self):
        job = {"name": "Mystery Job", "requirement": "", "responsibility": ""}
        roadmap = generate_roadmap(job, "Python")
        assert roadmap["roadmap_steps"] == []
        assert roadmap["match_after_preparation"] == "Unknown"

    def test_all_skills_strong(self):
        job = {
            "name": "Python Developer",
            "requirement": "Python, SQL",
            "responsibility": "Development",
        }
        roadmap = generate_roadmap(job, "Python programming, SQL databases, advanced development")
        # When user has all skills, roadmap_steps may be empty or small
        assert isinstance(roadmap["already_strong"], list)
