from textual.app import ComposeResult
from textual.containers import Center, Middle
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Label


class MainMenu(Screen):
    """The main menu screen for Luvinha."""

    BINDINGS = [("h", "how_to_play", "How to Play")]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=False)
        yield Footer()
        with Center():
            with Middle():
                yield Label("LUVINHA", id="title")
                yield Button("New Game", id="new-game", variant="primary")

    def action_how_to_play(self) -> None:
        from luvinha.screens.how_to_play import HowToPlay

        self.app.push_screen(HowToPlay())

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "new-game":
            self.app.exit(result="new-game")