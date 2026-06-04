from textual.screen import Screen

class BaseScreen(Screen):

    BINDINGS = [
        ("up", "focus_previous", "Focus Previous"),
        ("down", "focus_next", "Focus Next"),
    ]

    def action_focus_previous(self) -> None:
        self.focus_previous()

    def action_focus_next(self) -> None:
        self.focus_next()