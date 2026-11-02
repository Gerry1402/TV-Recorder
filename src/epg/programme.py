from datetime import datetime, timedelta

import humanize
from .parser import normalize


class Programme:
    def __init__(self, title: str, channel: str, start: datetime, end: datetime, description: str) -> None:
        self.title: str = title
        self.channel: str = channel
        self.start: datetime = start
        self.end: datetime = end
        self.description: str = description

    def on_air(self, time: datetime) -> bool:
        return self.start <= time < self.end

    def __str__(self) -> str:
        return f"{self.title} ({self.start:%d/%m/%Y}) ({self.start:%H:%M} - {self.end:%H:%M}) ({humanize.precisedelta(timedelta(seconds=len(self)))})"

    def __contains__(self, text: str) -> bool:
        return normalize(text) in normalize(self.title + self.description)

    def __len__(self) -> int:
        return (self.end - self.start).seconds

    def __repr__(self) -> str:
        content = {
            "title": self.title,
            "channel": self.channel,
            "start": humanize.precisedelta((datetime.now() - self.start) // timedelta(minutes=1) * timedelta(minutes=1)),
            "duration": humanize.precisedelta(timedelta(seconds=len(self))),
        }
        return "\nProgram(\n" + ",\n".join([f"\t{k}= {str(v)}" for k, v in content.items()]) + "\n\t)"
