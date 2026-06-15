from glove.validator import WordValidator, is_valid_word
from glove.glove import GloveModel


def test_validator_rejects_nonsense() -> None:
    WordValidator(GloveModel())
    assert is_valid_word("vvvvvv") is False
    assert is_valid_word("aaaaaa") is False
    assert is_valid_word("a") is False
    assert is_valid_word("ab") is False
    assert is_valid_word("casa") is True
    assert is_valid_word("123") is False
    assert is_valid_word("") is False