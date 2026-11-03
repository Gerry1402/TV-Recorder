import re

import humanize
from playwright.sync_api import Response

from .channels import CHANNELS
from .fragments import Fragments


class ResponseHandler:
    def __init__(self, channel: str, show: str) -> None:
        self.fragments = Fragments(channel, show)
        self.pattern = CHANNELS[channel]["pattern"]

    def is_filtered(self, resp: Response) -> bool:
        conditions = (
            re.fullmatch(self.pattern, resp.url) is not None,
            resp.status in (200, 206),
        )
        return all(conditions)

    @staticmethod
    def is_valid(resp: Response) -> bytes | None:
        try:
            content = resp.body()
        except Exception as e:
            print("Couldn't be read: ", resp.url, e)
            return None
        return content

    def on_response(self, resp: Response) -> None:
        if self.is_filtered(resp):
            if content := self.is_valid(resp):
                self.fragments.append(content)
                print(f"Fragment {len(self.fragments)} saved, {humanize.naturalsize(self.fragments.size())}        ", end="\r")
