from textual.app import ComposeResult

from .base_screen import BaseScreen
from textual.widgets import Label

class ClassicMode(BaseScreen):
    def compose(self) -> ComposeResult:
        yield Label("TODO")
