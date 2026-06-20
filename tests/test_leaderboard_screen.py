from __future__ import annotations

from app import LuvinhaApp
from app.screens.leaderboard import LeaderboardScreen
from leaderboard import Leaderboard


def _row_texts(screen) -> list[str]:
    return [
        str(w.content) for w in screen.query(".ranking-row") if hasattr(w, "content")
    ]


async def test_leaderboard_screen_shows_entries_ranked(tmp_path) -> None:
    lb = Leaderboard(db_path=tmp_path / "lb.db")
    lb.add("bob", "carro", 5)
    lb.add("ana", "gato", 3)
    app = LuvinhaApp(leaderboard=lb)
    async with app.run_test() as pilot:
        app.push_screen(LeaderboardScreen())
        await pilot.pause()
        texts = _row_texts(app.screen)
        assert len(texts) == 2
        assert "ana" in texts[0]
        assert "bob" in texts[1]
        assert app.screen.query_one("#empty-ranking").display is False


async def test_leaderboard_screen_empty_state(tmp_path) -> None:
    lb = Leaderboard(db_path=tmp_path / "lb.db")
    app = LuvinhaApp(leaderboard=lb)
    async with app.run_test() as pilot:
        app.push_screen(LeaderboardScreen())
        await pilot.pause()
        assert _row_texts(app.screen) == []
        assert app.screen.query_one("#empty-ranking").display is True


async def test_leaderboard_escape_returns(tmp_path) -> None:
    lb = Leaderboard(db_path=tmp_path / "lb.db")
    lb.add("ana", "gato", 3)
    app = LuvinhaApp(leaderboard=lb)
    async with app.run_test() as pilot:
        app.push_screen(LeaderboardScreen())
        await pilot.pause()
        await pilot.press("escape")
        await pilot.pause()
        from app.screens.main_menu import MainMenu

        assert isinstance(app.screen, MainMenu)
