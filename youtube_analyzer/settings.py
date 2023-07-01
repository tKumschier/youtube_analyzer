#
from pathlib import Path

from pydantic import BaseSettings


class Settings(BaseSettings):
    # API Key for Google
    api_key: str

    # Settings for Icloud
    icloud_id: str
    icloud_pass: str
    to_address: str
    subject: str = "YoutubeAnalyzer - Problem to download metadata"
    message: str = "Problem to download medatada:"

    class Config:
        env_file = Path(__file__).resolve().parent / "credentials.env"


settings = Settings()  # type: ignore
