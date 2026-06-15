from __future__ import annotations

import random
from pathlib import Path

import numpy as np
from huggingface_hub import hf_hub_download
from safetensors.numpy import load_file

from glove.validator import is_valid_word

REPO_ID = "nilc-nlp/glove-300d"
EMBEDDINGS_FILE = "embeddings.safetensors"
VOCAB_FILE = "vocab.txt"


class GloveModel:
    def __init__(self) -> None:
        self._vectors: np.ndarray | None = None
        self._vocab: list[str] = []
        self._word_to_index: dict[str, int] = {}

    @property
    def is_loaded(self) -> bool:
        return self._vectors is not None

    def load(self, cache_dir: str | Path | None = None) -> None:
        embeddings_path = hf_hub_download(
            repo_id=REPO_ID,
            filename=EMBEDDINGS_FILE,
            cache_dir=cache_dir,
        )
        data = load_file(embeddings_path)
        self._vectors = data["embeddings"]

        vocab_path = hf_hub_download(
            repo_id=REPO_ID,
            filename=VOCAB_FILE,
            cache_dir=cache_dir,
        )
        with open(vocab_path) as f:
            self._vocab = [line.strip() for line in f]

        self._word_to_index = {w: i for i, w in enumerate(self._vocab)}

    def similarity(self, word1: str, word2: str) -> float:
        if not self.is_loaded:
            raise RuntimeError("Model not loaded. Call load() first.")
        assert self._vectors is not None

        vec1 = self._get_vector(word1)
        vec2 = self._get_vector(word2)
        if vec1 is None or vec2 is None:
            return 0.0

        dot = float(np.dot(vec1, vec2))
        norm1 = float(np.linalg.norm(vec1))
        norm2 = float(np.linalg.norm(vec2))
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return dot / (norm1 * norm2)

    def most_similar(self, word: str, n: int = 10) -> list[tuple[str, float]]:
        if not self.is_loaded:
            raise RuntimeError("Model not loaded. Call load() first.")
        assert self._vectors is not None

        vec = self._get_vector(word)
        if vec is None:
            return []

        norms = np.linalg.norm(self._vectors, axis=1)
        dots = self._vectors @ vec
        cos_sim = dots / (norms * np.linalg.norm(vec))
        top_indices = np.argsort(cos_sim)[::-1][: n + 1]

        results: list[tuple[str, float]] = []
        word_idx = self._word_to_index.get(word, -1)
        for idx in top_indices:
            if idx == word_idx:
                continue
            results.append((self._vocab[idx], float(cos_sim[idx])))
            if len(results) == n:
                break
        return results

    def has_word(self, word: str) -> bool:
        return word in self._word_to_index

    def random_word(self) -> str:
        if not self.is_loaded:
            raise RuntimeError("Model not loaded. Call load() first.")
        eligible = [w for w in self._vocab if is_valid_word(w)]
        return random.choice(eligible)

    def _get_vector(self, word: str) -> np.ndarray | None:
        assert self._vectors is not None
        idx = self._word_to_index.get(word)
        if idx is None:
            return None
        return self._vectors[idx]