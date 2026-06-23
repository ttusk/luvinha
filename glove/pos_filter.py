from __future__ import annotations

from collections.abc import Iterable

import spacy

_nlp = None


def _get_nlp():
    global _nlp
    if _nlp is None:
        _nlp = spacy.load("pt_core_news_sm", disable=["parser", "ner", "lemmatizer"])
    return _nlp


def _is_base_form(token) -> bool:
    if token.pos_ == "NOUN":
        return "Number=Sing" in token.morph or not token.morph.get("Number")
    if token.pos_ == "VERB":
        return "VerbForm=Inf" in token.morph
    return False


def filter_by_pos(words: Iterable[str]) -> list[str]:
    texts = list(words)
    if not texts:
        return []
    nlp = _get_nlp()
    result: list[str] = []
    for word, doc in zip(texts, nlp.pipe(texts, batch_size=512)):
        if len(doc) == 1 and _is_base_form(doc[0]):
            result.append(word)
    return result