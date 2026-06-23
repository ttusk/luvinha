import pytest

from glove import GloveModel
from glove import glove as glove_module

RELATED_PAIRS = [
    ("garçom", "chef"),
    ("chef", "cozinha"),
    ("médico", "hospital"),
    ("pintor", "pincel"),
    ("professor", "escola"),
    ("pneu", "carro"),
    ("avião", "aeroporto"),
    ("livro", "biblioteca"),
]

ANTONYM_PAIRS = [
    ("quente", "frio"),
    ("grande", "pequeno"),
    ("bom", "mau"),
    ("claro", "escuro"),
]

UNRELATED_PAIRS = [
    ("banana", "carro"),
    ("elefante", "teclado"),
    ("martelo", "nuvem"),
    ("oculos", "pedra"),
]

NEAR_SYNONYM_PAIRS = [
    ("cachorro", "animal"),
    ("automóvel", "carro"),
    ("feliz", "alegre"),
    ("casa", "residência"),
]


def test_similarity_self_is_one(model: GloveModel) -> None:
    assert model.similarity("gato", "gato") == pytest.approx(1.0)


def test_similarity_related_vs_unrelated(model: GloveModel) -> None:
    assert model.similarity("gato", "cachorro") > model.similarity("gato", "carro")


@pytest.mark.parametrize("word1,word2", RELATED_PAIRS)
def test_similarity_related_above_threshold(model: GloveModel, word1: str, word2: str) -> None:
    assert model.similarity(word1, word2) > 0.25


@pytest.mark.parametrize("word1,word2", UNRELATED_PAIRS)
def test_similarity_unrelated_below_threshold(model: GloveModel, word1: str, word2: str) -> None:
    assert model.similarity(word1, word2) < 0.2


@pytest.mark.parametrize("word1,word2", ANTONYM_PAIRS)
def test_similarity_antonyms_still_correlated(model: GloveModel, word1: str, word2: str) -> None:
    assert model.similarity(word1, word2) > 0.3


@pytest.mark.parametrize("word1,word2", NEAR_SYNONYM_PAIRS)
def test_similarity_near_synonyms_above_related(model: GloveModel, word1: str, word2: str) -> None:
    assert model.similarity(word1, word2) > 0.35


@pytest.mark.parametrize("related,unrelated", [
    ((w1, w2), (u1, u2))
    for w1, w2 in RELATED_PAIRS
    for u1, u2 in UNRELATED_PAIRS
])
def test_related_always_higher_than_unrelated(model: GloveModel, related: tuple[str, str], unrelated: tuple[str, str]) -> None:
    assert model.similarity(*related) > model.similarity(*unrelated)


def test_most_similar_ranked_and_excludes_self(model: GloveModel) -> None:
    results = model.most_similar("gato", n=5)
    assert len(results) == 5
    words = [w for w, _ in results]
    assert "gato" not in words
    scores = [s for _, s in results]
    assert scores == sorted(scores, reverse=True)


def test_has_word(model: GloveModel) -> None:
    assert model.has_word("gato") is True
    assert model.has_word("xyzw1234") is False


def test_random_word_caches_eligible_list(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import numpy as np

    model = GloveModel()
    model._vocab = ["gato", "carro", "zzzz", "ab"]
    model._word_to_index = {w: i for i, w in enumerate(model._vocab)}
    model._vectors = np.zeros((4, 3))

    valid = {"gato", "carro"}
    calls = {"n": 0}

    def spy(word: str) -> bool:
        calls["n"] += 1
        return word in valid

    monkeypatch.setattr(glove_module, "is_valid_word", spy)
    monkeypatch.setattr(glove_module, "filter_by_pos", lambda ws: list(ws))

    assert model.random_word() in valid
    calls_after_first = calls["n"]

    assert model.random_word() in valid
    assert calls["n"] == calls_after_first


def test_random_word_restricts_to_most_frequent_top_n(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import numpy as np

    monkeypatch.setattr(glove_module, "FREQUENCY_TOP_N", 3)
    model = GloveModel()
    model._vocab = ["comum1", "comum2", "comum3", "raro"]
    model._word_to_index = {w: i for i, w in enumerate(model._vocab)}
    model._vectors = np.zeros((4, 3))

    monkeypatch.setattr(glove_module, "is_valid_word", lambda w: True)
    monkeypatch.setattr(glove_module, "filter_by_pos", lambda ws: list(ws))

    for _ in range(20):
        assert model.random_word() != "raro"