from __future__ import annotations

import sqlite3
from contextlib import closing
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_DB_PATH = Path.home() / ".luvinha" / "leaderboard.db"


@dataclass(frozen=True)
class ScoreEntry:
    username: str
    word: str
    attempts: int
    timestamp: str


class Leaderboard:
    """Armazena e consulta pontuações dos vencedores em SQLite."""

    def __init__(self, db_path: Path | None = None) -> None:
        self._path = Path(db_path) if db_path is not None else DEFAULT_DB_PATH
        self._ensure_schema()

    def _connect(self) -> sqlite3.Connection:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        return sqlite3.connect(self._path)

    def _ensure_schema(self) -> None:
        with closing(self._connect()) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS scores (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    word TEXT NOT NULL,
                    attempts INTEGER NOT NULL,
                    timestamp TEXT NOT NULL
                )
                """
            )
            conn.commit()

    def add(self, username: str, word: str, attempts: int) -> None:
        if not username or not username.strip():
            raise ValueError("username must not be empty")
        username = username.strip()
        with closing(self._connect()) as conn:
            conn.execute(
                "INSERT INTO scores (username, word, attempts, timestamp) "
                "VALUES (?, ?, ?, ?)",
                (username, word, attempts, datetime.now(timezone.utc).isoformat()),
            )
            conn.commit()

    def top(self, n: int = 10) -> list[ScoreEntry]:
        with closing(self._connect()) as conn:
            rows = conn.execute(
                "SELECT username, word, attempts, timestamp FROM scores "
                "ORDER BY attempts ASC, id ASC LIMIT ?",
                (n,),
            ).fetchall()
        return [ScoreEntry(r[0], r[1], r[2], r[3]) for r in rows]

    def is_empty(self) -> bool:
        with closing(self._connect()) as conn:
            (count,) = conn.execute("SELECT COUNT(*) FROM scores").fetchone()
        return count == 0
