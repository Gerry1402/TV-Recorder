from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Directories(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    output: Path = Path().home() / "Videos" / "TV"
    epg: Path = Path("EPGs")


directories = Directories()


class Urls(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    epg: str = "https://epgshare01.online/epgshare01/epg_ripper_ES1.xml.gz"


urls = Urls()
