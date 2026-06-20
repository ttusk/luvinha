from __future__ import annotations

import random

from textual.app import ComposeResult
from textual.containers import Center, Middle, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Footer, Label

GIVE_UP_MESSAGES = [
    "Quase lá! A próxima palavra é sua.",
    "A palavra era teimosa, hein?",
    "Palavras têm segredos — essa escapou.",
    "Bom palpite, mas o alvo venceu esta rodada.",
    "Não foi dessa vez. Que tal uma revanche?",
    "A sorte estava escondida entre as letras.",
]


class GiveUpScreen(ModalScreen[bool]):
    """Modal exibido ao desistir: revela a palavra alvo, tentativas e mensagem."""

    CSS_PATH = "give_up.tcss"

    BINDINGS = [
        ("escape", "dismiss_screen", "Voltar"),
        ("enter", "dismiss_screen", "Voltar"),
    ]

    def __init__(self, secret_word: str, attempts: int) -> None:
        super().__init__()
        self._secret = secret_word
        self._attempts = attempts

    def compose(self) -> ComposeResult:
        yield Footer()
        with Center():
            with Middle():
                with Vertical(id="give-up-dialog"):
                    yield Label("Fim de Jogo", id="give-up-title")
                    yield Label(random.choice(GIVE_UP_MESSAGES), id="give-up-message")
                    yield Label("A palavra secreta era:", id="give-up-hint")
                    yield Label(self._secret, id="secret-word")
                    yield Label(f"Tentativas: {self._attempts}", id="attempts")
                    yield Button("Voltar ao Menu", id="back-to-menu", variant="primary")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back-to-menu":
            self.dismiss(True)

    def action_dismiss_screen(self) -> None:
        self.dismiss(True)
