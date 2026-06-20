from __future__ import annotations

from app import LuvinhaApp
from app.screens.mode_selection import ModeSelection
from textual.widgets import Button


async def test_timed_mode_button_is_disabled_until_implemented() -> None:
    app = LuvinhaApp()
    async with app.run_test() as pilot:
        app.push_screen(ModeSelection())
        await pilot.pause()
        assert app.screen.query_one("#timed-mode", Button).disabled is True


async def test_classic_mode_button_is_enabled() -> None:
    app = LuvinhaApp()
    async with app.run_test() as pilot:
        app.push_screen(ModeSelection())
        await pilot.pause()
        assert app.screen.query_one("#classic-mode", Button).disabled is False
