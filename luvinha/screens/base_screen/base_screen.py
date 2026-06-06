from __future__ import annotations

from typing import TYPE_CHECKING

from textual.screen import Screen

if TYPE_CHECKING:
    from luvinha.app import LuvinhaApp


class BaseScreen(Screen):

    BINDINGS = [
        ("up", "focus_previous", "Anterior"),
        ("down", "focus_next", "Próximo"),
    ]

    def action_focus_previous(self) -> None:
        self.focus_previous()

    def action_focus_next(self) -> None:
        self.focus_next()

    @property
    def luvinha_app(self) -> LuvinhaApp:
        return self.app  # type: ignore[return-value]
