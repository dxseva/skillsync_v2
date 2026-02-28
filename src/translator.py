"""
Russian → English translator using Helsinki-NLP opus-mt model.
Handles batching and caching for efficiency.
"""
import re
from functools import lru_cache
from typing import Optional

_pipeline = None


def _get_pipeline():
    global _pipeline
    if _pipeline is None:
        from transformers import pipeline as hf_pipeline
        _pipeline = hf_pipeline(
            task="translation_ru_to_en",
            model="Helsinki-NLP/opus-mt-ru-en",
            device=-1,  # CPU
        )
    return _pipeline


def _contains_cyrillic(text: str) -> bool:
    return bool(re.search(r"[а-яёА-ЯЁ]", text))


def translate_ru_to_en(text: Optional[str], max_length: int = 512) -> str:
    """Translate Russian text to English. Returns original if no Cyrillic detected."""
    if not text or not text.strip():
        return ""

    text = text.strip()

    # Don't waste time translating already-English text
    if not _contains_cyrillic(text):
        return text

    try:
        pipe = _get_pipeline()
        # Chunk long texts to avoid truncation loss
        chunks = _split_text(text, max_chars=400)
        translated_parts = []
        for chunk in chunks:
            result = pipe(chunk, max_length=max_length, truncation=True)
            translated_parts.append(result[0]["translation_text"].strip())
        return " ".join(translated_parts)
    except Exception as e:
        print(f"[Translator] failed: {e}")
        return text  # return original rather than empty


def _split_text(text: str, max_chars: int = 400) -> list:
    """Split text into chunks at sentence boundaries."""
    if len(text) <= max_chars:
        return [text]

    sentences = re.split(r"(?<=[.!?;])\s+", text)
    chunks = []
    current = ""
    for s in sentences:
        if len(current) + len(s) + 1 <= max_chars:
            current = (current + " " + s).strip()
        else:
            if current:
                chunks.append(current)
            current = s
    if current:
        chunks.append(current)
    return chunks or [text[:max_chars]]


def translate_batch(texts: list) -> list:
    """Translate a list of texts, skipping non-Cyrillic ones."""
    return [translate_ru_to_en(t) for t in texts]
