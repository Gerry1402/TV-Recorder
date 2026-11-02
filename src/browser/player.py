import time
from datetime import datetime, timedelta

import humanize

from .browser import Stream
from .channels import CHANNELS
from .response import ResponseHandler as RespHandler
from .starter import Starter


class Player:
    margin: timedelta = timedelta(seconds=60)

    def __init__(self, channel: str, show: str) -> None:
        self.channel, self.show = channel, show
        self.resp: RespHandler = RespHandler(channel, show)
        self.player: Starter = Starter(channel)

    def record(self, start: datetime, end: datetime):
        while (start - self.margin) > datetime.now():
            wait = start - datetime.now() - self.margin
            print(f"Waiting {humanize.precisedelta(wait, format = "%0.0f")} until '{self.show}' starts...    ", end="\r")
            time.sleep(1)

        with Stream(self.channel).page as page:
            page.on("response", self.resp.on_response)
            page.goto(CHANNELS[self.channel]["url"], wait_until="domcontentloaded")
            self.player.prepare(page, self.resp.is_filtered)
            page.wait_for_timeout(end - datetime.now() + self.margin)
