from typing import Callable

from playwright.sync_api import Page

from .channels import CHANNELS


class Starter:
    between_clicks = 0.2  # seconds
    adds = 90  # seconds

    def __init__(self, channel: str) -> None:
        self.selectors: dict[str, str] = CHANNELS[channel]["selectors"].copy()
        self.css_player: str = self.selectors.pop("player")
        self.coordinates: tuple[tuple[float, float], tuple[float, float]] | None = None

    def prepare(self, page: Page, filter: Callable) -> None:

        def obtain_coordinates() -> tuple[tuple[float, float], tuple[float, float]]:
            player = page.locator(self.css_player)
            box = player.bounding_box()
            if box is None:
                raise ValueError("The bounding box of the player could not be obtained.")
            return (box["x"], box["y"]), (box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)

        def hover(start: tuple[float, float], end: tuple[float, float]) -> None:
            page.mouse.move(*start)
            page.mouse.move(*end, steps=20)

        def start_stream(filter: Callable) -> None:
            with page.expect_response(lambda r: filter(r), timeout=self.adds * 1000) as _:
                page.locator(self.selectors["start"]).click()
            self.coordinates = obtain_coordinates()

        def click(selector: str) -> None:
            if self.coordinates:
                hover(*self.coordinates)
            page.wait_for_timeout(self.between_clicks * 1000)
            page.locator(self.selectors[selector]).click()

        for elem in self.selectors:
            click(elem) if elem != "start" else start_stream(filter)
