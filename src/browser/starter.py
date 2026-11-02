from typing import Callable

from playwright.sync_api import Page

from .channels import CHANNELS


class Starter:
    between_clicks = 0.1  # seconds
    adds = 60  # seconds
    after_play = 3

    def __init__(self, channel: str) -> None:
        self.selectors: dict[str, str] = CHANNELS[channel]["selectors"]

    def prepare(self, page: Page, filter: Callable) -> None:

        if self.selectors.get("startfirst"):
            with page.expect_response(lambda r: filter(r), timeout=self.adds * 1000) as _:
                page.locator(self.selectors.pop("start")).click()
            page.wait_for_timeout(self.after_play * 1000)

        player = page.locator(self.selectors["player"])
        box = player.bounding_box()
        if box is None:
            raise ValueError("No se pudo obtener el bounding box del reproductor.")
        cx = box["x"] + box["width"] / 2
        cy = box["y"] + box["height"] / 2

        def action(selector: str) -> None:
            try:
                page.mouse.move(box["x"], box["y"])
                page.mouse.move(cx, cy, steps=20)
                page.wait_for_timeout(self.between_clicks * 1000)
                player.locator(self.selectors[selector]).click()
            except Exception as e:
                print(f"Error al ejecutar la acción {selector}: {e}")
                return

        for event in ["message", "start", "mute", "fullscreen"]:
            if event in self.selectors:
                if event != "start":
                    action(event)
                else:
                    with page.expect_response(lambda r: filter(r), timeout=self.adds * 1000) as _:
                        action(event)
                    page.wait_for_timeout(self.after_play * 1000)
