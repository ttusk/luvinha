import pytest

from glove.pos_filter import filter_by_pos

pytestmark = pytest.mark.slow


def test_filter_by_pos_keeps_singular_nouns_and_infinitive_verbs() -> None:
    words = ["casa", "correr", "bonito", "rapidamente", "gato"]
    result = filter_by_pos(words)
    assert "casa" in result
    assert "correr" in result
    assert "gato" in result
    assert "bonito" not in result
    assert "rapidamente" not in result


def test_filter_by_pos_rejects_conjugated_verbs() -> None:
    words = ["transmitida", "correndo", "comeu", "comer", "cantar"]
    result = filter_by_pos(words)
    assert "comer" in result
    assert "cantar" in result
    assert "transmitida" not in result
    assert "correndo" not in result
    assert "comeu" not in result


def test_filter_by_pos_rejects_plural_nouns() -> None:
    words = ["casa", "casas", "gato", "gatos"]
    result = filter_by_pos(words)
    assert "casa" in result
    assert "gato" in result
    assert "casas" not in result
    assert "gatos" not in result


def test_filter_by_pos_empty_input() -> None:
    assert filter_by_pos([]) == []


def test_filter_by_pos_empty_output() -> None:
    result = filter_by_pos([" muito"])
    assert result == []


def test_filter_by_pos_single_token_only() -> None:
    result = filter_by_pos(["casa grande"])
    assert result == []