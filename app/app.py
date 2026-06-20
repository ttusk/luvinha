from textual.app import App
from textual.reactive import reactive
from app.screens.main_menu import MainMenu
from app.screens.classic_mode import ClassicMode
from leaderboard import Leaderboard


class LuvinhaApp(App[None]):
    """O jogo Luvinha."""

    selected_mode = reactive("classic-mode")

    TITLE = "Luvinha"
    CSS_PATH = "styles.tcss"
    ENABLE_COMMAND_PALETTE = False

    SCREENS = {"main_menu": MainMenu, "classic_mode": ClassicMode}

    def __init__(self, leaderboard: Leaderboard | None = None) -> None:
        super().__init__()
        self._leaderboard: Leaderboard | None = leaderboard

    @property
    def leaderboard(self) -> Leaderboard:
        if self._leaderboard is None:
            self._leaderboard = Leaderboard()
        return self._leaderboard

    def on_mount(self) -> None:
        self.theme = "solarized-light"
        self.push_screen("main_menu")