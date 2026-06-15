from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Label, ProgressBar


class GuessItem(Vertical):

    CSS_PATH = "guess_item.tcss"

    def __init__(
        self,
        word: str,
        score: int,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)
        self._word = word
        self._score = score

    def compose(self) -> ComposeResult:
        yield Label(self._word, id="guess-word")
        yield ProgressBar(
            total=1000,
            show_percentage=False,
            show_eta=False,
            id="guess-progress",
        )
        yield Label(str(self._score), id="guess-score")

    def on_mount(self) -> None:
        self.query_one(ProgressBar).update(progress=self._score)