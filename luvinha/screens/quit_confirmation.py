from textual.app import ComposeResult
from textual.containers import Center, Middle
from textual.widgets import Button, Footer, Header, Label
from luvinha.screens.base_screen import BaseScreen

class QuitConfirmation(BaseScreen):
    """Tela de confirmação para sair do jogo."""

    BINDINGS = BaseScreen.BINDINGS + [("y", "confirm_quit", "Sim"), ("n", "cancel_quit", "Não")]

    def compose(self) -> ComposeResult:
        yield Footer()
        with Center():
            with Middle():
                yield Label("Tem certeza que deseja sair?", id="quit-confirmation")
                yield Button("Sim", id="confirm-yes", variant="error", flat=True)
                yield Button("Não", id="confirm-no", variant="primary", flat=True)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "confirm-yes":
            self.app.exit(result="quit")
        elif event.button.id == "confirm-no":
            self.app.pop_screen()

    def action_confirm_quit(self) -> None:
        self.app.exit(result="quit")

    def action_cancel_quit(self) -> None:
        self.app.pop_screen()
