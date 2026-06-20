from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Center, Middle, Vertical, VerticalScroll
from textual.screen import ModalScreen
from textual.widgets import Button, Footer, Label


class CheatScreen(ModalScreen[None]):
    """Modal secreto: mostra as palavras mais próximas da palavra alvo."""

    CSS_PATH = "cheat.tcss"

    BINDINGS = [
        ("escape", "close", "Fechar"),
        ("enter", "close", "Fechar"),
    ]

    def __init__(self, hints: list[tuple[str, float]]) -> None:
        super().__init__()
        self._hints = hints

    def compose(self) -> ComposeResult:
        yield Footer()
        with Center():
            with Middle():
                with Vertical(id="cheat-dialog"):
                    yield Label("Dicas", id="cheat-title")
                    yield Label("Palavras mais próximas do alvo:", id="cheat-hint")
                    with VerticalScroll(id="cheat-list"):
                        for word, score in self._hints:
                            yield Label(
                                f"{word} ({round(score * 1000)})",
                                classes="cheat-row",
                            )
                    yield Button("Fechar", id="cheat-close", variant="primary")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "cheat-close":
            self.dismiss(None)

    def action_close(self) -> None:
        self.dismiss(None)
