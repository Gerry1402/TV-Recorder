from datetime import datetime
from pathlib import Path

from config import directories

from .channels import CHANNELS


def norm(text: str) -> str:
    replacements = {
        "?": "ʔ",
        "*": "⋆",
        "<": "‹",
        ">": "›",
        "–": "-",
        ":": "꞉",
        "\\": "＼",
        "/": "／",
        "​": "",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    return text


class Fragments:
    def __init__(self, channel: str, show: str) -> None:
        self.path: Path = (directories.output / norm(channel) / norm(show) / datetime.now().strftime(r"%Y-%m-%d")).with_suffix(
            CHANNELS[channel]["suffix"]
        )
        self.num: int = 0

    def append(self, content: bytes) -> None:
        self.path.parent.mkdir(exist_ok=True, parents=True)
        with self.path.open("ab") as f:
            f.write(content)
        self.num += 1

    def __len__(self) -> int:
        return self.num

    def size(self) -> int:
        if self.path.exists():
            return self.path.stat().st_size
        return 0
