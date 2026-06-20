from __future__ import annotations

from app import LuvinhaApp
from app.screens.how_to_play import HowToPlay


async def test_how_to_play_widget_ids_are_unique() -> None:
    app = LuvinhaApp()
    async with app.run_test() as pilot:
        app.push_screen(HowToPlay())
        await pilot.pause()
        ids = [w.id for w in app.screen.walk_children() if w.id]
        assert ids, "expected some widgets with ids"
        assert len(ids) == len(set(ids))


async def test_how_to_play_shows_instructions() -> None:
    app = LuvinhaApp()
    async with app.run_test() as pilot:
        app.push_screen(HowToPlay())
        await pilot.pause()
        labels = [
            str(w.content) for w in app.screen.walk_children() if hasattr(w, "content")
        ]
        assert any("Adivinhe a palavra secreta" in text for text in labels)
        assert any("semanticamente" in text for text in labels)
