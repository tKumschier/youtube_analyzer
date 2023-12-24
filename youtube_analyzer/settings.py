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
    data_path: Path = Path(__file__).resolve().parents[1] / "data"
    log_level: str = "INFO"

    class Config:
        env_file = Path(__file__).resolve().parents[1] / "settings.env"


settings = Settings()  # type: ignore
