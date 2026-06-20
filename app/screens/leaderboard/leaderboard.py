from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical, VerticalScroll
from textual.widgets import Header, Footer, Label

from app.screens.base_screen import BaseScreen


class LeaderboardScreen(BaseScreen):
    """Tela do ranking dos vencedores."""

    CSS_PATH = "leaderboard.tcss"

    BINDINGS = BaseScreen.BINDINGS + [("escape", "go_back", "Voltar")]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=False)
        yield Footer()
        with Vertical(id="leaderboard-container"):
            yield Label("Ranking", id="leaderboard-title")
            yield Label(
                "Nenhuma pontuação registrada ainda.",
                id="empty-ranking",
            )
            yield VerticalScroll(id="ranking-list")

    def on_mount(self) -> None:
        entries = self.app.leaderboard.top(n=50)
        if not entries:
            return
        self.query_one("#empty-ranking").display = False
        listing = self.query_one("#ranking-list", VerticalScroll)
        for rank, entry in enumerate(entries, start=1):
            listing.mount(
                Label(
                    f"{rank}. {entry.username} — {entry.word} "
                    f"({entry.attempts} tentativas)",
                    classes="ranking-row",
                )
            )

    def action_go_back(self) -> None:
        self.app.pop_screen()
