from textual.app import App
from textual.reactive import reactive
from luvinha.screens.main_menu.main_menu import MainMenu
from luvinha.screens.classic_mode.classic_mode import ClassicMode
from luvinha.screens.mode_selection.mode_selection import ModeSelection
from luvinha.screens.quit_confirmation.quit_confirmation import QuitConfirmation


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
