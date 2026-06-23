from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Label

BAR_WIDTH = 10


def _build_bar(score: int) -> str:
    filled = max(0, min(BAR_WIDTH, round(score / 100)))
    return "\u2588" * filled + "\u2591" * (BAR_WIDTH - filled)


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
        row = f"{self._word:<12}\u2192 {self._score:>4}  {_build_bar(self._score)}"
        yield Label(row, id="guess-row")