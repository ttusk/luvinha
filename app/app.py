from textual.app import App
from textual.reactive import reactive
from app.screens.main_menu import MainMenu
from app.screens.classic_mode import ClassicMode


class LuvinhaApp(App[None]):
    """O jogo Luvinha."""

    selected_mode = reactive("classic-mode")

    TITLE = "Luvinha"
    CSS_PATH = "styles.tcss"
    ENABLE_COMMAND_PALETTE = False

    SCREENS = {"main_menu": MainMenu, "classic_mode": ClassicMode}

    def on_mount(self) -> None:
        self.theme = "solarized-light"
        self.push_screen("main_menu")