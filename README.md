# SkillSync Pro v2

SkillSync Pro v2 is an AI-powered career matching system built on live vacancy data from HeadHunter (HH.ru). It combines multilingual semantic search, real-time API aggregation, and skill gap analysis to generate ranked job recommendations and structured learning roadmaps.

The repository contains:

- A Streamlit MVP application ([`app.py`](./app.py))
- A FastAPI backend service ([`backend/`](./backend))
- A shared AI engine in [`src/`](./src)
- Basic test coverage in [`tests/`](./tests)

The system is designed around deterministic ranking logic layered on top of transformer embeddings, with clear separation between data acquisition, scoring, translation, and roadmap generation.

---

## Architecture Overview

The system is divided into four main components:

### 1. Live Vacancy Aggregation  
[`src/fetcher.py`](./src/fetcher.py) retrieves jobs from HH.ru using `requests` and a multi-query search strategy with experience-level expansion.

### 2. Multilingual Semantic Ranking  
[`src/recommender.py`](./src/recommender.py) uses Sentence Transformers to compute cosine similarity between user goals and vacancy content.

### 3. Translation for Display  
[`src/translator.py`](./src/translator.py) translates Russian snippets to English for UI readability only. Scoring is performed directly on multilingual embeddings.

### 4. Skill Gap & Roadmap Generation  
[`src/roadmap.py`](./src/roadmap.py) extracts required skills, evaluates coverage using vector similarity, and estimates preparation timelines.

The FastAPI layer in [`backend/main.py`](./backend/main.py) exposes `/api/search` and `/api/roadmap`, while the Streamlit app orchestrates the same engine in a single-process flow.

---

## Interesting Techniques Used

### Multilingual Semantic Matching (No Pre-Translation Required)

Uses:

- [sentence-transformers](https://www.sbert.net/)
- Model: `paraphrase-multilingual-mpnet-base-v2`

English user queries are compared directly against Russian vacancy text in a shared embedding space. This avoids translation bias and simplifies the scoring pipeline.

---

### Heuristic Query Expansion

[`src/fetcher.py`](./src/fetcher.py) expands free-text user input by:

- Extracting role tokens
- Mapping English goal phrases to Russian equivalents
- Querying across multiple experience filters

This improves recall without introducing probabilistic generation.

---

### In-Memory Embedding Cache

[`src/embedding_cache.py`](./src/embedding_cache.py)

Embeddings are cached using MD5 hashes of input text. Only uncached strings are processed by the transformer model, reducing redundant computation across ranking and roadmap evaluation.

---

### Deterministic Roadmap Classification via Cosine Similarity

The roadmap engine:

- Extracts skills from job requirements
- Computes similarity between job skills and user skills
- Classifies coverage (strong / partial / missing)
- Applies time estimates based on required level and user learning capacity

No generative LLM is used for roadmap logic. Outputs are reproducible.

---

### Chunked Transformer Translation

[`src/translator.py`](./src/translator.py)

Uses:

- [transformers](https://huggingface.co/docs/transformers/index)
- Model: [Helsinki-NLP/opus-mt-ru-en](https://huggingface.co/Helsinki-NLP/opus-mt-ru-en)

Long text is split into sentence-based chunks (~400 characters) to reduce truncation during inference.

---

### FastAPI with Environment-Based CORS

[`backend/main.py`](./backend/main.py)

CORS is configured using:

- [FastAPI](https://fastapi.tiangolo.com/)
- [CORSMiddleware](https://fastapi.tiangolo.com/tutorial/cors/)

Allowed origins are controlled via the `CORS_ORIGINS` environment variable.

---

## Notable Libraries & Technologies

- [sentence-transformers](https://www.sbert.net/)
- [transformers (Hugging Face)](https://huggingface.co/docs/transformers/index)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Pydantic](https://docs.pydantic.dev/)
- [requests](https://docs.python-requests.org/)
- [Streamlit](https://streamlit.io/)
- [pytest](https://docs.pytest.org/)

External API:

- HeadHunter API: https://api.hh.ru/vacancies

---

## Project Structure

```
.
├── app.py
├── backend/
├── frontend/
├── src/
├── tests/
```

### backend/
FastAPI API layer exposing search and roadmap endpoints.

### frontend/
React client that consumes the FastAPI service.

### src/
Core AI engine modules:
- live vacancy fetching
- semantic ranking
- translation
- roadmap generation
- configuration definitions

### tests/
Basic tests for fetcher and recommender logic.

---

## Running the Project

### 1. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it:

**macOS / Linux**
```bash
source .venv/bin/activate
```

**Windows**
```bash
.venv\Scripts\activate
```

---

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

The first run will download transformer models automatically.

---

## Option A — Run Streamlit MVP

```bash
streamlit run app.py
```

The app will start locally in your browser.

---

## Option B — Run FastAPI Backend

```bash
uvicorn backend.main:app --reload --port 8000
```

API endpoints:

- `GET  http://localhost:8000/api/cities`
- `POST http://localhost:8000/api/search`
- `POST http://localhost:8000/api/roadmap`

---

## Optional — Run Frontend

If using the React frontend:

```bash
cd frontend
npm install
npm run dev
```

Make sure the backend is running and CORS origins are configured if needed:

```bash
export CORS_ORIGINS="http://localhost:5173"
```

---

## Running Tests

```bash
pytest -q
```

---

## Design Goals

- Deterministic ranking layered on transformer embeddings
- Live vacancy integration
- Minimal hallucination surface
- Clear separation of concerns (fetch → rank → translate → roadmap)
- Stateless API layer
- Shared engine for Streamlit and FastAPI modes
