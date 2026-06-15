from textual.reactive import reactive
from textual.app import ComposeResult
from textual.containers import Grid, Horizontal, VerticalScroll, Vertical
from textual.validation import Length
from textual.widgets import (
    Header,
    Footer,
    Label,
    Input,
    Button,
    LoadingIndicator,
)

from app.screens.base_screen import BaseScreen
from app.screens.classic_mode.guess_item import GuessItem
from glove import GloveModel, WordValidator


class ClassicMode(BaseScreen):
    """Tela do modo clássico de jogo."""

    CSS_PATH = "classic_mode.tcss"

    BINDINGS = BaseScreen.BINDINGS + [("escape", "go_back", "Voltar")]

    maior_proximidade = reactive(None)
    melhor_palpite = reactive("")
    tentativas = reactive(0)
    guesses = reactive({})

    def on_mount(self) -> None:
        self.glove = GloveModel()
        self.run_worker(self.glove.load, name="load_glove", thread=True)

    def compose(self) -> ComposeResult:
        yield Header(show_clock=False)
        yield Footer()

        with Vertical(id="game-container"):
            with Horizontal(id="input-bar"):
                yield Input(
                    placeholder="Digite uma palavra...",
                    id="guess-input",
                    type="text",
                    validators=[Length(minimum=1)],
                    disabled=True,
                )
                yield Button("Desistir", id="give-up", variant="error", disabled=True)

            with Horizontal(id="status-bar"):
                yield Label("Tentativas: 0", id="attempts")
                yield Label("Melhor: - (-)", id="best-rank")

            yield LoadingIndicator(id="loading-indicator")
            with VerticalScroll(id="ranking"):
                yield Grid(id="ranking-grid")

    def on_worker_state_changed(self, event) -> None:
        if event.worker.name == "load_glove" and event.worker.is_finished:
            self.secret_word = self.glove.random_word()
            self._validator = WordValidator(self.glove)
            self.maior_proximidade = None
            self.tentativas = 0
            self.melhor_palpite = ""
            self.guesses = {}
            self.watch(self, "tentativas", self.update_attempts)
            self.watch(self, "maior_proximidade", self.update_best_rank)
            self.watch(self, "guesses", self.update_ranking)
            self.query_one("#loading-indicator", LoadingIndicator).display = False
            self.query_one("#guess-input", Input).disabled = False
            self.query_one("#give-up", Button).disabled = False
            self.query_one("#guess-input", Input).focus()

    def update_attempts(self, tentativas: int) -> None:
        self.query_one("#attempts", Label).update(f"Tentativas: {tentativas}")

    def update_best_rank(self, maior_proximidade: int) -> None:
        self.query_one("#best-rank", Label).update(
            f"Melhor: {self.melhor_palpite if self.melhor_palpite else '-'} ({maior_proximidade if maior_proximidade else '-'})"
        )

    def update_ranking(self, guesses: dict[str, int]) -> None:
        grid = self.query_one("#ranking-grid", Grid)
        grid.remove_children()
        for palavra, prox in sorted(guesses.items(), key=lambda x: x[1], reverse=True):
            grid.mount(GuessItem(word=palavra, score=prox))

    def on_input_submitted(self, event: Input.Submitted) -> None:
        guess = event.value.strip().lower()
        if not guess or guess in self.guesses:
            return

        if not self.glove.is_loaded or not self._validator.is_known(guess):
            self._show_invalid_word()
            return

        self.tentativas += 1
        proximity = self.glove.similarity(guess, self.secret_word)
        score = round(proximity * 1000)

        self.guesses = {**self.guesses, guess: score}

        if self.maior_proximidade is None or score > self.maior_proximidade:
            self.melhor_palpite = guess
            self.maior_proximidade = score

        self.query_one("#guess-input", Input).value = ""

    def _show_invalid_word(self) -> None:
        input_widget = self.query_one("#guess-input", Input)
        original_placeholder = input_widget.placeholder
        input_widget.placeholder = "Palavra não reconhecida"
        input_widget.value = ""

        def restore() -> None:
            input_widget.placeholder = original_placeholder

        self.set_timer(1.5, restore)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "give-up":
            from app.screens.quit_confirmation import QuitConfirmation
            self.app.push_screen(QuitConfirmation())

    def action_go_back(self) -> None:
        self.app.pop_screen()