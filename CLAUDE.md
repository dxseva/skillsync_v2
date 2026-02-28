# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

SkillSync Pro v2 is an AI-powered career guide for university students and recent graduates. It fetches live vacancies from the HH.ru API (Russian job board), semantically matches them to a user's career goal using multilingual embeddings, and generates a personalized skill gap roadmap. The UI is a Streamlit app with a 4-step conversational flow.

## Commands

```bash
# Install dependencies (uses CPU-only PyTorch)
pip install -r requirements.txt

# Run the app (opens at http://localhost:8501)
streamlit run app.py
```

First run downloads ~500MB of models: `paraphrase-multilingual-mpnet-base-v2` (embeddings) and `Helsinki-NLP/opus-mt-ru-en` (translation).

## Architecture

The app is a single-page Streamlit application (`app.py`) with a 4-step session-state-driven flow: `goal → profile → results → roadmap`.

**`app.py`** — Streamlit UI and session state management. All steps are in one file, gated by `st.session_state.step`. Custom CSS for dark theme is embedded inline. Imports from `src/` are done lazily inside step blocks to avoid loading ML models until needed.

**`src/config.py`** — Central constants: model names, API base URL, `EN_TO_RU_QUERIES` mapping (60+ English career keywords → Russian HH.ru search terms), `CITY_AREA_IDS` (city→HH area ID mapping), `SKILL_NOISE_WORDS` (soft-skill filter list), `SKILL_LEVEL_TIME` dict mapping skill levels to `(min_months, max_months)` tuples.

**`src/fetcher.py`** — HH.ru REST API client. Builds search queries from free-text English input by stripping stop words, augmented with Russian queries from `EN_TO_RU_QUERIES`. Supports city filtering via `CITY_AREA_IDS` and relocation logic. Includes `fetch_vacancy_details()` for structured key_skills from individual vacancy endpoints. Iterates across multiple experience levels and pages per query. Deduplicates by vacancy ID. Raises `HHApiError` on connection issues. Rate-limited with 0.3s delays.

**`src/embedding_cache.py`** — Dict-based embedding cache using MD5 hashes. Avoids re-encoding duplicate texts across recommender and roadmap calls.

**`src/recommender.py`** — Semantic scoring using `SentenceTransformer` (`paraphrase-multilingual-mpnet-base-v2`) with `EmbeddingCache`. Builds an enriched user query from goal + profile, encodes all job texts via cache, ranks by cosine similarity. Applies soft penalties (e.g., senior roles demoted for students) and format boosts.

**`src/roadmap.py`** — Skill gap analysis. Extracts skill phrases from job text with noise filtering (`SKILL_NOISE_WORDS`). Prioritizes structured `key_skills` from the HH API when available. Computes per-skill coverage via batch cosine similarity against user's stated skills. Classifies each skill as "already strong" (>=0.72), "improve" (>=0.48), or "learn from scratch". Generates time estimates using `SKILL_LEVEL_TIME` with a parallelism factor adjusted by user's self-assessed skill level. Realistic `match_after` based on actual similarity scores. Includes curated `SKILL_RESOURCES` dict mapping skill domains to learning resources.

**`src/translator.py`** — Russian→English translation via `Helsinki-NLP/opus-mt-ru-en` pipeline. Lazily loaded. Skips text without Cyrillic characters. Chunks long text at sentence boundaries to avoid truncation.

### Language Strategy

The app operates in three language layers:

1. **Search layer**: English queries (from user input) + Russian queries (from `EN_TO_RU_QUERIES` mapping) are sent to HH.ru API. This maximizes vacancy coverage since most HH.ru listings are in Russian.
2. **Matching layer**: The multilingual embedding model (`paraphrase-multilingual-mpnet-base-v2`) handles English↔Russian matching natively — no translation needed for semantic scoring.
3. **Display layer**: Russian job snippets are translated to English via `Helsinki-NLP/opus-mt-ru-en` for display only. Translation happens after ranking, not before.

### Key Design Patterns

- **Lazy model loading**: Both the SentenceTransformer and translation pipeline are loaded on first use and cached in module-level globals (`_model`, `_pipeline`).
- **Embedding cache**: `EmbeddingCache` prevents re-encoding the same text strings across recommender and roadmap calls.
- **Multilingual bridging**: The multilingual embedding model handles English↔Russian matching natively — translation is only used for display, not for semantic scoring.
- **No database**: All state lives in Streamlit session state. No persistence between sessions.
- **No auth required**: HH.ru API is public but rate-limited.

## Dependencies

Python 3.12 with CPU-only PyTorch. Key packages: `streamlit`, `sentence-transformers`, `transformers`, `requests`, `torch` (CPU), `sentencepiece`, `sacremoses`, `pytest`.

## Testing

```bash
pytest tests/ -v
```

Tests cover query building, Russian query lookup, area resolution, semantic ranking quality, skill extraction, noise filtering, and roadmap structure.
