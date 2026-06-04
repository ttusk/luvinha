from textual.app import ComposeResult
from textual.containers import Center, Middle
from textual.widgets import Button, Footer, Header, Label
from luvinha.screens.base_screen import BaseScreen


class MainMenu(BaseScreen):
    """Tela do menu principal do Luvinha."""

    BINDINGS = BaseScreen.BINDINGS + [("h", "how_to_play", "Como Jogar"), ("escape", "quit", "Sair")]

    def on_mount(self) -> None:
        self.query_one("#new-game", Button).focus()
        self.watch(self.app, "selected_mode", self.update_mode)

    def compose(self) -> ComposeResult:
        yield Header(show_clock=False)
        yield Footer()
        with Center():
            with Middle():
                yield Label("LUVINHA", id="title")
                yield Label("", id="mode-info")
                yield Button("Novo Jogo", id="new-game", variant="primary")
                yield Button("Selecionar Modo", id="mode-selection", variant="primary")


    def update_mode(self, mode: str):
        self.query_one("#mode-info", Label).update(
            f"Modo Selecionado: {mode}"
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "new-game":
            self.app.exit(result="new-game")
        elif event.button.id == "mode-selection":
            from luvinha.screens.mode_selection import ModeSelection

            self.app.push_screen(ModeSelection())

    def action_how_to_play(self) -> None:
        from luvinha.screens.how_to_play import HowToPlay

        self.app.push_screen(HowToPlay())

    def action_quit(self) -> None:
        from luvinha.screens.quit_confirmation import QuitConfirmation

        self.app.push_screen(QuitConfirmation())
