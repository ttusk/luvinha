from __future__ import annotations

from pathlib import Path

import pytest

from leaderboard import Leaderboard, ScoreEntry


def test_add_and_top_orders_by_fewest_attempts(tmp_path: Path) -> None:
    lb = Leaderboard(db_path=tmp_path / "lb.db")
    lb.add("ana", "gato", 5)
    lb.add("bob", "gato", 3)
    lb.add("carol", "gato", 7)
    top = lb.top(n=10)
    assert [e.username for e in top] == ["bob", "ana", "carol"]
    assert all(e.word == "gato" for e in top)


def test_top_limits_to_n(tmp_path: Path) -> None:
    lb = Leaderboard(db_path=tmp_path / "lb.db")
    for i in range(5):
        lb.add(f"u{i}", "gato", i + 1)
    assert len(lb.top(n=3)) == 3


def test_persists_across_instances(tmp_path: Path) -> None:
    path = tmp_path / "lb.db"
    Leaderboard(db_path=path).add("ana", "gato", 4)
    lb2 = Leaderboard(db_path=path)
    assert [e.username for e in lb2.top()] == ["ana"]


def test_is_empty(tmp_path: Path) -> None:
    lb = Leaderboard(db_path=tmp_path / "lb.db")
    assert lb.is_empty()
    lb.add("ana", "gato", 4)
    assert not lb.is_empty()


def test_rejects_empty_username(tmp_path: Path) -> None:
    lb = Leaderboard(db_path=tmp_path / "lb.db")
    with pytest.raises(ValueError):
        lb.add("", "gato", 4)


def test_entries_expose_fields(tmp_path: Path) -> None:
    lb = Leaderboard(db_path=tmp_path / "lb.db")
    lb.add("ana", "gato", 2)
    entry = lb.top()[0]
    assert isinstance(entry, ScoreEntry)
    assert entry.username == "ana"
    assert entry.word == "gato"
    assert entry.attempts == 2
    assert entry.timestamp
