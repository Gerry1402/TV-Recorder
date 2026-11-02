import gzip
from datetime import datetime
from pathlib import Path

from curl_cffi import requests

from config import directories, urls


class XMLManager:
    now = datetime.now()

    def __init__(self) -> None:
        self.path: Path = (directories.epg / self.now.date().isoformat()).with_suffix(".xml")

    def get_or_update(self) -> Path:
        if not self.path.exists():
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self.download()
        return self.path

    def download(self) -> None:
        response = requests.get(urls.epg)
        response.raise_for_status()
        xml_bytes = gzip.decompress(response.content)
        with self.path.open("wb") as f:
            f.write(xml_bytes)
