import json
import os
from pathlib import Path

from dotenv import load_dotenv

from youtube_analyzer.utils.logger import logger
from youtube_analyzer.utils.yapi import YApi


def get_channel_id_list() -> list[str]:
    json_file_path = Path(__file__).resolve().parent / "channels_to_parse.json"
    with open(json_file_path, "r", encoding="utf-8") as json_file:
        channel_ids = json.load(json_file)

    return list(channel_ids.values())


def get_api_key() -> str:
    load_dotenv(Path(__file__).resolve().parent / "credentials.env")
    api_key: str = os.environ.get("api_key")
    return api_key


def main():
    try:
        logger.info("Start youtube_analyzer")
        api_key = get_api_key()
        channel_id = get_channel_id_list()
        yapi = YApi(api_key=api_key, channel_ids=channel_id)
        yapi.perform_request()
        logger.info("Finish")
    except Exception as exception:
        logger.warning(exception)
