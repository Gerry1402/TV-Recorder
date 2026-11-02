import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

from sortedcontainers import SortedDict

from .channel import Channel
from .file import XMLManager
from .parser import normalize, parse_programme
from .programme import Programme


class EPG:
    def __init__(self) -> None:
        self.channels: dict[str, Channel] = SortedDict()
        self.from_xml(XMLManager().get_or_update())

    def __getitem__(self, name: str) -> Channel:
        return self.channels[normalize(name)]

    def __iter__(self):
        return iter(self.channels.values())

    def __len__(self) -> int:
        return len(self.channels)

    def __contains__(self, name: str) -> bool:
        return normalize(name) in self.channels.keys()

    def search(self, text: str) -> list[Channel]:
        t = normalize(text)
        return sorted({c for c in self if t in normalize(c.name)}, key=lambda c: c.name)

    def on_air(self) -> dict[str, Programme | None]:
        return SortedDict({c.name: c.on_air(datetime.now()) for c in self})

    def __str__(self) -> str:
        return f"EPG ({len(self.channels)} channels and {sum(len(c) for c in self)} programs)"

    def __repr__(self) -> str:
        return f"EPG (channels={len(self.channels)})"

    def from_xml(self, path: Path) -> None:
        root = ET.parse(path).getroot()
        for p in root.findall("programme"):
            ptv = Programme(**parse_programme(p))
            self.channels.setdefault(normalize(ptv.channel), Channel(ptv.channel)).add(ptv)


if __name__ == "__main__":
    epg = EPG()
    for programme in epg["Cuatro"]:
        print(programme)
