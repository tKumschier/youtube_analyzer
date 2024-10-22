import json
from pathlib import Path

from miscellaneous.logger import logger
from miscellaneous.send_mail import send_mail
from youtube_analyzer.settings import settings
from youtube_analyzer.utils.yapi import YApi


def get_channel_id_list() -> list[str]:
    json_file_path = Path(__file__).resolve().parent / "channels_to_parse.json"
    with open(json_file_path, "r", encoding="utf-8") as json_file:
        channel_ids = json.load(json_file)

    return list(channel_ids.values())


def main():
    try:
        logger.replace_handlers()
        logger.info("Start youtube_analyzer")
        channel_id = get_channel_id_list()
        yapi = YApi(api_key=settings.api_key, channel_ids=channel_id)
        yapi.perform_request()
        logger.info("Finish")
    except Exception as exception:  # pylint: disable=broad-exception-caught
        logger.warning(exception)
    finally:
        if logger.problem_occurred and settings.send_error_email:
            send_mail(
                icloud_id=settings.icloud_id,
                icloud_pass=settings.icloud_pass,
                to_address=settings.to_address,
                subject=settings.subject,
                message=settings.message,
                files=[logger.save_path],
            )
