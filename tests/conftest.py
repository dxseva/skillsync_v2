import pytest


@pytest.fixture
def sample_profile():
    return {
        "skills": "Python, SQL, basic machine learning, English B2",
        "year": 3,
        "format": "any",
        "relocation": False,
        "city": "Any city",
        "skill_level": "intermediate",
    }


@pytest.fixture
def sample_profile_graduate():
    return {
        "skills": "Java, Spring Boot, PostgreSQL, REST APIs",
        "year": 0,
        "format": "remote",
        "relocation": True,
        "city": "Москва",
        "skill_level": "intermediate",
    }


@pytest.fixture
def sample_jobs():
    return [
        {
            "id": "101",
            "name": "Junior Python Developer",
            "url": "https://hh.ru/vacancy/101",
            "employer": "TechCorp",
            "area": "Москва",
            "requirement": "Python, Django, REST API, SQL, Git",
            "responsibility": "Develop backend services, write tests, code review",
            "salary": {"from": 80000, "to": 120000, "currency": "RUR"},
            "schedule": "Удалённая работа",
            "experience": "Нет опыта",
        },
        {
            "id": "102",
            "name": "Senior Data Engineer",
            "url": "https://hh.ru/vacancy/102",
            "employer": "DataInc",
            "area": "Санкт-Петербург",
            "requirement": "5+ years Python, Spark, Airflow, advanced SQL, Kubernetes",
            "responsibility": "Design data pipelines, lead team, architect solutions",
            "salary": {"from": 300000, "to": 500000, "currency": "RUR"},
            "schedule": "Полный день",
            "experience": "От 3 до 6 лет",
        },
        {
            "id": "103",
            "name": "Data Analyst Intern",
            "url": "https://hh.ru/vacancy/103",
            "employer": "StartupXYZ",
            "area": "Москва",
            "requirement": "SQL, Excel, basic Python, statistics",
            "responsibility": "Analyze data, build dashboards, prepare reports",
            "salary": None,
            "schedule": "Удалённая работа",
            "experience": "Нет опыта",
        },
        {
            "id": "104",
            "name": "Fullstack Developer",
            "url": "https://hh.ru/vacancy/104",
            "employer": "WebAgency",
            "area": "Новосибирск",
            "requirement": "React, Node.js, TypeScript, PostgreSQL",
            "responsibility": "Develop web applications, implement features",
            "salary": {"from": 150000, "to": None, "currency": "RUR"},
            "schedule": "Гибкий график",
            "experience": "От 1 до 3 лет",
        },
    ]


@pytest.fixture
def sample_key_skills():
    return [
        {"name": "Python"},
        {"name": "Django"},
        {"name": "PostgreSQL"},
        {"name": "REST API"},
        {"name": "Git"},
        {"name": "Docker"},
    ]
