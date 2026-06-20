from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Center, Horizontal, Middle, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Footer, Input, Label
from textual.validation import Length

from leaderboard import Leaderboard


class WinScreen(ModalScreen[bool]):
    """Modal de vitória: revela a palavra, registra o username no ranking."""

    CSS_PATH = "win.tcss"

    BINDINGS = [("escape", "skip", "Pular")]

    def __init__(
        self,
        secret_word: str,
        attempts: int,
        leaderboard: Leaderboard,
    ) -> None:
        super().__init__()
        self._secret = secret_word
        self._attempts = attempts
        self._leaderboard = leaderboard

    def compose(self) -> ComposeResult:
        yield Footer()
        with Center():
            with Middle():
                with Vertical(id="win-dialog"):
                    yield Label("Você Venceu!", id="win-title")
                    yield Label("A palavra secreta era:", id="win-hint")
                    yield Label(self._secret, id="secret-word")
                    yield Label(f"Tentativas: {self._attempts}", id="attempts")
                    yield Input(
                        placeholder="Seu nome para o ranking",
                        id="username",
                        validators=[Length(minimum=1)],
                    )
                    with Horizontal(id="win-buttons"):
                        yield Button(
                            "Salvar no Ranking", id="save-score", variant="success"
                        )
                        yield Button("Pular", id="skip-save", variant="default")

    def on_mount(self) -> None:
        self.query_one("#username", Input).focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save-score":
            self._save()
        elif event.button.id == "skip-save":
            self.dismiss(False)

    def action_skip(self) -> None:
        self.dismiss(False)

    def _save(self) -> None:
        username = self.query_one("#username", Input).value.strip()
        if not username:
            self.query_one("#username", Input).placeholder = "Digite um nome válido"
            self.query_one("#username", Input).focus()
            return
        self._leaderboard.add(username, self._secret, self._attempts)
        self.dismiss(True)
