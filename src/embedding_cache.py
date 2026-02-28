"""
Embedding cache: avoids re-encoding the same texts across calls.
Uses MD5 hash of text as cache key.
"""
import hashlib
from typing import List

import numpy as np


def _text_hash(text: str) -> str:
    return hashlib.md5(text.encode("utf-8")).hexdigest()


class EmbeddingCache:
    """Dict-based cache for sentence embeddings."""

    def __init__(self):
        self._cache: dict = {}  # hash → numpy array

    def encode(self, model, texts: List[str], **kwargs) -> np.ndarray:
        """
        Encode texts using the model, returning cached results where available.
        Uncached texts are batch-encoded and added to the cache.
        """
        if not texts:
            return np.array([])

        hashes = [_text_hash(t) for t in texts]
        cached_indices = []
        uncached_indices = []

        for i, h in enumerate(hashes):
            if h in self._cache:
                cached_indices.append(i)
            else:
                uncached_indices.append(i)

        # Batch-encode uncached texts
        if uncached_indices:
            uncached_texts = [texts[i] for i in uncached_indices]
            # Force numpy output for cache storage
            encode_kwargs = {**kwargs}
            encode_kwargs.pop("convert_to_tensor", None)
            new_embs = model.encode(
                uncached_texts,
                normalize_embeddings=True,
                show_progress_bar=False,
                batch_size=kwargs.get("batch_size", 32),
            )
            for idx, emb in zip(uncached_indices, new_embs):
                self._cache[hashes[idx]] = emb

        # Assemble results in original order
        result = np.array([self._cache[hashes[i]] for i in range(len(texts))])
        return result

    def clear(self):
        self._cache.clear()
