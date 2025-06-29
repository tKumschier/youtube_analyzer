import json
from datetime import datetime
from pathlib import Path
from typing import Any

from pydantic import BaseModel

from miscellaneous.logger import logger
from youtube_analyzer.schema.data import Data
from youtube_analyzer.settings import settings


class DataHandler(BaseModel):
    data_subpath: Path

    def __init__(self, **data: Any) -> None:
        current_date: str = datetime.now().strftime("%Y.%m.%d")
        current_time: str = datetime.now().strftime("%H.00")
        data_subpath: Path = settings.data_path / current_date / current_time
        data_subpath.mkdir(parents=True, exist_ok=True)
        super().__init__(data_subpath=data_subpath, **data)

    def save_to_json(self, data: Data) -> None:
        save_path: Path = self.data_subpath / f"{data.channel_item.id}.json"
        with open(save_path, "w", encoding="UTF-8") as json_file:
            json.dump(data.dict(), json_file, indent=4)
        logger.info(f"Save to {save_path}")
