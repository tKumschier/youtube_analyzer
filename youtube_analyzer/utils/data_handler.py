import json
from datetime import datetime
from pathlib import Path
from typing import Any

from pydantic import BaseModel

from youtube_analyzer.schema.data import Data
from youtube_analyzer.utils.logger import logger


class DataHandler(BaseModel):
    root_path: Path

    def __init__(self, **data: Any) -> None:
        folder_name: str = datetime.now().strftime("%Y.%m.%d_%H.00")
        root_path: Path = Path(__file__).resolve().parents[2] / "data" / folder_name
        root_path.mkdir(parents=True, exist_ok=True)
        super().__init__(root_path=root_path, **data)

    def save_to_json(self, data: Data) -> None:
        save_path: Path = self.root_path / f"{data.channel_item.id}.json"
        with open(save_path, "w", encoding="UTF-8") as json_file:
            json.dump(data.dict(), json_file, indent=4)
        logger.info(f"Save to {save_path}")
