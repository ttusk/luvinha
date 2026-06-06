from textual.app import ComposeResult
from textual.containers import Center, Middle, Vertical
from textual.screen import ModalScreen
from textual.widgets import Footer, Label


class HowToPlay(ModalScreen[None]):
    """Modal explicando como jogar."""

    BINDINGS = [("escape", "close", "Fechar")]

    def compose(self) -> ComposeResult:
        with Center():
            with Middle():
                with Vertical(id="how-to-play-dialog"):
                    yield Label("Como Jogar")
                    yield Label("Em breve!")
                    yield Footer()

    def action_close(self) -> None:
        self.dismiss(None)
