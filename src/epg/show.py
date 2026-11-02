from datetime import date, datetime

from sortedcontainers import SortedSet

from .parser import normalize
from .programme import Programme


class Show:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.programs: set[Programme] = SortedSet(key=lambda p: p.start)

    def __iter__(self):
        return iter(self.programs)

    def __len__(self) -> int:
        return len(self.programs)

    def __str__(self) -> str:
        return f"{self.name} ({len(self)} program{'' if len(self.programs) == 1 else 's'})"

    def __repr__(self) -> str:
        return f"Show(nombre={self.name!r}, programs={len(self.programs)})"

    def __contains__(self, text: str) -> bool:
        return normalize(text) in normalize(self.name)

    def actual(self) -> Programme | None:
        now = datetime.now()
        for p in self:
            if now < p.end:
                return p
            if p.start > now:
                return p
        return None

    def add(self, program: Programme) -> None:
        self.programs.add(program)
