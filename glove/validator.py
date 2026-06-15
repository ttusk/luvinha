from __future__ import annotations

from spellchecker import SpellChecker


_SPELL = SpellChecker(language="pt")


def is_valid_word(word: str) -> bool:
    if not word or len(word) < 2:
        return False
    return word.lower() in _SPELL.known({word.lower()})


class WordValidator:

    def __init__(self, glove_model):
        self._glove = glove_model

    def is_known(self, word: str) -> bool:
        return is_valid_word(word) and self._glove.has_word(word)