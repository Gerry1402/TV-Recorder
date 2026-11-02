import unicodedata
from datetime import datetime
from xml.etree.ElementTree import Element


def normalize(text: str, save: list[tuple[str, str]] = []) -> str:
    text = unicodedata.normalize("NFC", "".join(text.lower().split()).strip())
    text = text.replace("ñ", "\0")
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    return text.replace("\0", "ñ")


def norm(text: str) -> str:
    return " ".join(text.strip().split())


def text(element: Element, tag: str) -> str:
    return norm(element.findtext(tag, default=""))


def get(element: Element, attr: str) -> str:
    return norm(element.get(attr, default=""))


def parse_programme(element: Element) -> dict:
    return {
        "title": text(element, "title"),
        "description": text(element, "desc") or text(element, "sub-title"),
        "channel": get(element, "channel")[:-2]
        .replace("..", "\0")
        .replace(".", " ")
        .replace("\0", ". ")
        .replace("Campeones.", "Campeones")
        .strip(),
        "start": datetime.strptime(get(element, "start").split()[0], r"%Y%m%d%H%M%S"),
        "end": datetime.strptime(get(element, "stop").split()[0], r"%Y%m%d%H%M%S"),
    }
