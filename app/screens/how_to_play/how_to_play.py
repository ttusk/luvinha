from textual.app import ComposeResult
from textual.containers import Center, Middle, Vertical
from textual.screen import ModalScreen
from textual.widgets import Label


class HowToPlay(ModalScreen[None]):
    """Modal explicando como jogar."""

    CSS_PATH = "how_to_play.tcss"

    BINDINGS = [("escape", "close", "Fechar")]

    def compose(self) -> ComposeResult:
        with Center():
            with Middle():
                with Vertical(id="how-to-play-dialog"):
                    yield Label("Como Jogar", id="how-to-play-title")
                    yield Label("Adivinhe a palavra secreta.", classes="how-to-play-line")
                    yield Label(
                        "Quanto mais próxima semanticamente, maior a pontuação.",
                        classes="how-to-play-line",
                    )

    def action_close(self) -> None:
        self.dismiss(None)