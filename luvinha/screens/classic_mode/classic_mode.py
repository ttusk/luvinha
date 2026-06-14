from textual import on
from textual.reactive import reactive
from textual.app import ComposeResult
from textual.containers import Horizontal, VerticalScroll
from textual.validation import Length
from textual.widgets import (
    Header,
    Footer,
    Label,
    Input,
    Button,
    DataTable
)

from luvinha.screens.base_screen.base_screen import BaseScreen

from ..base_screen.base_screen import BaseScreen
from textual.widgets import Label

class ClassicMode(BaseScreen, VerticalScroll):
    def on_mount(self) -> None:
        self.watch(self, "tentativas", self.update_attempts)
        self.watch(self, "maior_proximidade", self.update_best_rank)
        self.maior_proximidade = None
        self.tentativas = 0
        self.query_one("#ranking", DataTable).clear()

    def compose(self) -> ComposeResult:
        yield Header(show_clock=False)

        with Horizontal(id="status-bar"):
            yield Label("Modo: Clássico", id="game-mode")
            yield Label(f"Tentativas: {self.tentativas}", id="attempts")
            yield Label(f"Melhor posição: {self.maior_proximidade if self.maior_proximidade else 'N/A'}, Palpite: {self.melhor_palpite if self.melhor_palpite else 'N/A'}", id="best-rank")

        yield Input(
            placeholder="Digite uma palavra...",
            id="guess-input",
            type="text",
            validators=[Length(minimum=1)]
        )

        yield Button(
            "Desistir",
            id="give-up",
            variant="error"
        )

        yield Label("Ranking de proximidade")

        table = DataTable(id="ranking", show_cursor=False, cursor_type="none")
        table.add_columns(
            "#",
            "Palavra",
            "Proximidade"
        )

        yield table

        yield Footer()
    
    def update_attempts(self, tentativas: int) -> None:
        self.query_one("#attempts", Label).update(
            f"Tentativas: {tentativas}"
        )

    def update_best_rank(self, maior_proximidade: int) -> None:
        self.query_one("#best-rank", Label).update(
            f"Maior proximidade: {maior_proximidade if maior_proximidade else 'N/A'}, Palpite: {self.melhor_palpite if self.melhor_palpite else 'N/A'}"
        )

    CSS_PATH = "classic_mode.tcss"
    
    BUTTONS = BaseScreen.BINDINGS

    FAKE_SIMILARITIES = {
        "gato": 950,
        "cachorro": 870,
        "animal": 720,
        "pet": 690,
        "carro": 80,
        "casa": 150,
    }

    maior_proximidade = reactive(None)
    melhor_palpite = reactive("")
    tentativas = reactive(0)
    tentativas_list = reactive([])

    def on_input_submitted(
        self,
        event: Input.Submitted
    ) -> None:
        guess = event.value.strip().lower()
        if not guess:
            return
        
        self.tentativas += 1

        # Pegar proximidade do glove
        proximidade = self.FAKE_SIMILARITIES.get(guess, 0)

        self.tentativas_list.append((guess, proximidade))

        if self.maior_proximidade is None or proximidade > self.maior_proximidade:
            self.melhor_palpite = guess
            self.maior_proximidade = proximidade

        # Atualiza a tabela de ranking
        ranking_table = self.query_one("#ranking", DataTable)
        ranking_table.clear()
        for i, (palavra, prox) in enumerate(sorted(self.tentativas_list, key=lambda x: x[1], reverse=True), start=1):
            ranking_table.add_row(str(i), palavra, str(prox))

        self.query_one("#guess-input", Input).value = ""

    def on_button_pressed(
        self,
        event: Button.Pressed
    ) -> None:
        if event.button.id == "give-up":
            from luvinha.screens.quit_confirmation.quit_confirmation import QuitConfirmation
            #Implementar confirmação de desistência, por enquanto é apenas quit
            self.app.push_screen(QuitConfirmation())