from textual.screen import Screen

class BaseScreen(Screen):

    BINDINGS = [
        ("up", "focus_previous", "Focar Anterior"),
        ("down", "focus_next", "Focar Próximo"),
        ("b", "maybe_pop", "Voltar")
    ]

    def action_focus_previous(self) -> None:
        self.focus_previous()

    def action_focus_next(self) -> None:
        self.focus_next()

    def action_maybe_pop(self):
        if len(self.app.screen_stack) > 1:
            self.app.pop_screen()
