"""Tests for src/fetcher.py — query building, Russian query lookup, area resolution."""
from src.fetcher import _build_queries, _get_russian_queries, _resolve_area


class TestBuildQueries:
    def test_simple_role(self):
        queries = _build_queries("data scientist", {"year": 0})
        assert any("data" in q and "scientist" in q for q in queries)

    def test_verbose_input(self):
        queries = _build_queries("Hey I want to become a Python developer", {"year": 3})
        assert any("python" in q for q in queries)

    def test_junior_variant_for_students(self):
        queries = _build_queries("developer", {"year": 2})
        assert any("junior" in q for q in queries)

    def test_no_junior_for_graduates(self):
        queries = _build_queries("developer", {"year": 0})
        assert not any("junior" in q for q in queries)

    def test_max_queries_limit(self):
        queries = _build_queries("machine learning engineer data scientist", {"year": 3})
        assert len(queries) <= 8

    def test_empty_goal(self):
        queries = _build_queries("", {"year": 0})
        # Should not crash; may return empty or Russian-only queries
        assert isinstance(queries, list)

    def test_includes_russian_queries(self):
        queries = _build_queries("lawyer", {"year": 0})
        # Should include Russian queries from EN_TO_RU_QUERIES
        has_russian = any(any(ord(c) > 127 for c in q) for q in queries)
        assert has_russian, f"Expected Russian queries for 'lawyer', got: {queries}"


class TestGetRussianQueries:
    def test_known_keyword(self):
        ru = _get_russian_queries("python developer")
        assert len(ru) > 0
        assert any("python" in q.lower() or "разработчик" in q for q in ru)

    def test_unknown_keyword(self):
        ru = _get_russian_queries("xyznonexistent")
        assert ru == []

    def test_multiple_matches(self):
        ru = _get_russian_queries("data analyst")
        assert len(ru) >= 2

    def test_deduplication(self):
        ru = _get_russian_queries("lawyer attorney")
        # Both map to "адвокат" and "юрист" — should deduplicate
        assert len(ru) == len(set(ru))


class TestResolveArea:
    def test_any_city_returns_none(self):
        assert _resolve_area({"city": "Any city"}) is None

    def test_relocation_returns_none(self):
        assert _resolve_area({"city": "Москва", "relocation": True}) is None

    def test_known_city(self):
        assert _resolve_area({"city": "Москва", "relocation": False}) == "1"
        assert _resolve_area({"city": "Санкт-Петербург", "relocation": False}) == "2"

    def test_empty_city(self):
        assert _resolve_area({"city": "", "relocation": False}) is None
