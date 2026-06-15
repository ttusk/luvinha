from textual.app import ComposeResult
from textual.containers import Center, Middle, Vertical
from textual.widgets import Button, Footer, Header, Label
from app.screens.base_screen import BaseScreen


class ModeSelection(BaseScreen):
    """Tela de seleção de modo do Luvinha."""

    CSS_PATH = "mode_selection.tcss"

    BINDINGS = BaseScreen.BINDINGS + [("escape", "go_back", "Voltar")]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=False)
        yield Footer()
        with Center():
            with Middle():
                yield Label("Selecionar Modo de Jogo", id="mode-title")
                with Vertical(id="mode-buttons"):
                    yield Button("Modo Clássico", id="classic-mode", variant="primary")
                    yield Button("Modo Cronometrado", id="timed-mode", variant="primary")

    def on_mount(self) -> None:
        self.query_one("#classic-mode", Button).focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id is not None:
            self.luvinha_app.selected_mode = event.button.id
        self.app.pop_screen()

    def action_go_back(self) -> None:
        self.app.pop_screen()