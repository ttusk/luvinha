from textual.app import ComposeResult
from textual.containers import Center, Middle
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Label
from luvinha.screens.base_screen import BaseScreen
from luvinha.screens.main_menu import MainMenu

class QuitConfirmation(BaseScreen):
    """A confirmation screen for quitting the game."""

    BINDINGS = BaseScreen.BINDINGS + [("y", "confirm_quit", "Yes"), ("n", "cancel_quit", "No")]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=False)
        yield Footer()
        with Center():
            with Middle():
                yield Label("Are you sure you want to quit?", id="quit-confirmation")
                yield Button("Yes", id="confirm-yes", variant="error")
                yield Button("No", id="confirm-no", variant="primary")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "confirm-yes":
            self.app.exit(result="quit")
        elif event.button.id == "confirm-no":
            self.app.pop_screen()

    def action_confirm_quit(self) -> None:
        self.app.exit(result="quit")

    def action_cancel_quit(self) -> None:
        self.app.pop_screen()