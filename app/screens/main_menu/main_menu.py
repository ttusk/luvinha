from textual.app import ComposeResult
from textual.containers import Center, Middle, Vertical
from textual.widgets import Button, Footer, Label
from app.screens.base_screen import BaseScreen
from app.screens.classic_mode import ClassicMode


class MainMenu(BaseScreen):
    """Tela do menu principal do Luvinha."""

    CSS_PATH = "main_menu.tcss"

    BINDINGS = BaseScreen.BINDINGS + [
        ("h", "how_to_play", "Como Jogar"),
        ("escape", "quit", "Sair"),
    ]

    def compose(self) -> ComposeResult:
        yield Footer()
        with Center():
            with Middle():
                yield Label("LUVINHA", id="title")
                with Vertical(id="menu-buttons"):
                    yield Button("Novo Jogo", id="new-game", variant="primary")
                    yield Button("Selecionar Modo", id="mode-selection", variant="primary")
                    yield Button("Ranking", id="leaderboard", variant="default")

    def on_mount(self) -> None:
        self.query_one("#new-game", Button).focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "new-game":
            self.app.push_screen(ClassicMode())
        elif event.button.id == "mode-selection":
            from app.screens.mode_selection import ModeSelection
            self.app.push_screen(ModeSelection())
        elif event.button.id == "leaderboard":
            from app.screens.leaderboard import LeaderboardScreen
            self.app.push_screen(LeaderboardScreen())

    def action_how_to_play(self) -> None:
        from app.screens.how_to_play import HowToPlay
        self.app.push_screen(HowToPlay())

    def action_quit(self) -> None:
        from app.screens.quit_confirmation import QuitConfirmation
        self.app.push_screen(QuitConfirmation())