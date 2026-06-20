from __future__ import annotations

import pytest

from app import LuvinhaApp
from app.screens.classic_mode import classic_mode as classic_mode_module
from app.screens.classic_mode import ClassicMode
from app.screens.main_menu import MainMenu
from textual.widgets import Input, Label

class FakeGloveModel:
    """In-memory stand-in for GloveModel so UI tests need no 1.12 GB download."""

    def __init__(self, secret: str = "gato") -> None:
        self.is_loaded = True
        self._secret = secret
        self._known = {"gato", "cachorro", "carro", "felino", "leao"}

    def load(self, cache_dir: object = None) -> None:
        return None

    def random_word(self) -> str:
        return self._secret

    def has_word(self, word: str) -> bool:
        return word in self._known

    def similarity(self, word1: str, word2: str) -> float:
        return 1.0 if word1 == word2 else 0.42


async def _start_game(pilot, secret: str = "gato") -> None:
    """Drive the real 'Novo Jogo' flow and wait for the guess input to enable."""
    await pilot.click("#new-game")
    for _ in range(100):
        await pilot.pause(0.02)
        screen = pilot.app.screen
        if isinstance(screen, ClassicMode):
            try:
                if not screen.query_one("#guess-input", Input).disabled:
                    return
            except Exception:
                pass
    raise AssertionError("ClassicMode did not become ready in time")


async def test_escape_returns_to_main_menu(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(classic_mode_module, "GloveModel", FakeGloveModel)
    app = LuvinhaApp()
    async with app.run_test() as pilot:
        await _start_game(pilot)
        await pilot.press("escape")
        await pilot.pause()
        assert isinstance(app.screen, MainMenu)


async def _submit_guess(pilot, word: str) -> None:
    screen = pilot.app.screen
    assert isinstance(screen, ClassicMode)
    screen.query_one("#guess-input", Input).value = word
    await pilot.press("enter")
    await pilot.pause()


async def test_give_up_reveals_secret_and_returns_to_menu(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(classic_mode_module, "GloveModel", FakeGloveModel)
    app = LuvinhaApp()
    async with app.run_test() as pilot:
        await _start_game(pilot)
        await _submit_guess(pilot, "cachorro")

        await pilot.click("#give-up")
        await pilot.pause()

        results = app.screen
        assert "gato" in str(results.query_one("#secret-word", Label).content)
        assert "1" in str(results.query_one("#attempts", Label).content)

        await pilot.click("#back-to-menu")
        await pilot.pause()
        assert isinstance(app.screen, MainMenu)
        assert app.is_running


async def test_invalid_word_placeholder_restores_after_rapid_input(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(classic_mode_module, "GloveModel", FakeGloveModel)
    app = LuvinhaApp()
    async with app.run_test() as pilot:
        await _start_game(pilot)
        screen = app.screen
        assert isinstance(screen, ClassicMode)

        await _submit_guess(pilot, "xyzw")
        await pilot.pause(0.05)
        await _submit_guess(pilot, "zzzz")
        await pilot.pause(0.05)
        assert (
            screen.query_one("#guess-input", Input).placeholder
            == classic_mode_module.INVALID_PLACEHOLDER
        )

        await pilot.pause(2.0)
        assert (
            screen.query_one("#guess-input", Input).placeholder
            == "Digite uma palavra..."
        )
