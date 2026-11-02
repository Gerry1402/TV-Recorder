from __future__ import annotations

from datetime import date, datetime

from sortedcontainers import SortedDict

from .parser import normalize
from .programme import Programme
from .show import Show


class Channel:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.shows: "dict[str, Show]" = SortedDict()

    def on_air(self, time: datetime) -> Programme | None:
        for p in self:
            if p.on_air(time):
                return p
        return None

    def now(self) -> Programme | None:
        return self.on_air(datetime.now())

    def next(self) -> Programme | None:
        if pn := self.now():
            for p in self:
                if p.on_air(pn.end):
                    return p
        return None

    def today(self) -> list[Programme]:
        return [p for p in self if p.start.date() == date.today()]

    def future(self) -> list[Programme]:
        return [p for p in self if p.start > datetime.now()]

    def __contains__(self, text: str) -> bool:
        return normalize(text) in self.shows.keys()

    def search(self, text: str) -> list[Programme]:
        return sorted(
            [p for p in self if text in p],
            key=lambda p: (normalize(text) in normalize(p.title), p.start),
        )

    def __iter__(self):
        return iter(sorted([p for s in self.shows.values() for p in s], key=lambda p: p.start))

    def __len__(self) -> int:
        return len(self.shows)

    def __str__(self) -> str:
        return f"{self.name} ({len(self)} program{'' if len(self.shows) == 1 else 's'})"

    def __repr__(self) -> str:
        return f"Channel(nombre={self.name!r}, programs={len(self.shows)})"

    def __getitem__(self, title: str) -> Show:
        return self.shows[normalize(title)]

    def add(self, program: Programme) -> None:
        self.shows.setdefault(normalize(program.title), Show(program.title)).add(program)
