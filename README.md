# SkillSync Pro v2

AI-powered career guide for university students and recent graduates.
Fetches real vacancies from HH.ru (Russian job board), matches them semantically
to your career goal using multilingual embeddings, and builds a personalized
skill gap roadmap.

---

## Features

- **Live HH.ru API** — fetches real, current vacancies (no stale cache)
- **Bilingual search** — English queries + Russian translations from 60+ career keyword mappings for maximum coverage
- **Semantic matching** — `paraphrase-multilingual-mpnet-base-v2` ranks jobs by meaning across languages, not keywords
- **Auto-translation** — Russian job snippets are translated to English for display using `Helsinki-NLP/opus-mt-ru-en`
- **City filtering** — 25+ supported cities with relocation toggle
- **Smart profiling** — adapts to your year of study, skill level, city, work format, and existing skills
- **Structured skills** — fetches key_skills from HH.ru API for accurate gap analysis
- **Gap analysis** — compares your skills vs job requirements using vector similarity with noise filtering
- **Personalized roadmap** — step-by-step learning plan with time estimates adjusted by skill level
- **Embedding cache** — avoids redundant ML model calls for repeated texts
- **Conversational UI** — 4-step guided flow, mobile-friendly dark theme

---

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

> First run downloads two models (~500MB total):
> - `paraphrase-multilingual-mpnet-base-v2` (sentence embeddings)
> - `Helsinki-NLP/opus-mt-ru-en` (Russian → English translation)

### 2. Run

```bash
streamlit run app.py
```

Then open http://localhost:8501

### 3. Run tests

```bash
pytest tests/ -v
```

---

## Architecture

```
app.py                  # Streamlit UI — 4-step conversational flow
src/
  config.py             # Constants, model names, city IDs, noise words, skill timings
  fetcher.py            # HH.ru API client with bilingual queries + key_skills fetching
  translator.py         # Helsinki-NLP ru→en translation pipeline
  recommender.py        # Semantic scoring with EmbeddingCache + soft filters
  embedding_cache.py    # MD5-keyed embedding cache for performance
  roadmap.py            # Skill gap analysis + personalized learning roadmap
tests/
  test_fetcher.py       # Query building, Russian lookups, area resolution
  test_ranking.py       # Semantic ranking quality, penalties, boosts
  test_roadmap.py       # Skill extraction, noise filtering, roadmap structure
```

### Language Strategy

The app uses three language layers:

1. **Search**: English + Russian queries sent to HH.ru API for maximum coverage
2. **Matching**: Multilingual embeddings handle cross-language similarity natively
3. **Display**: Russian snippets translated to English via Helsinki-NLP model

---

## Notes

- HH.ru API is public (no auth required) but rate-limited; app adds polite delays
- Models are cached in memory after first load (fast subsequent searches)
- Translation quality is good for technical/professional Russian; may be imperfect for colloquial text
- Roadmap time estimates assume ~10–15 hours/week of study
- Parallelism factor adjusts based on user's self-assessed skill level
