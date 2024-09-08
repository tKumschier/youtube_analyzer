# mypy: disable-error-code="attr-defined"
import json
from pathlib import Path
from typing import Any, Dict, List

from googleapiclient.discovery import Resource, build
from googleapiclient.http import HttpRequest
from tenacity import RetryCallState, retry, stop_after_attempt, wait_fixed

from miscellaneous.logger import logger
from youtube_analyzer.schema.channels import Channels, ChannelsItem
from youtube_analyzer.schema.data import Data
from youtube_analyzer.schema.playlist_items import PlaylistItems, PlaylistItemsItem
from youtube_analyzer.schema.videos import Videos
from youtube_analyzer.utils.data_handler import DataHandler


def retry_write_log_message(retry_state: RetryCallState):
    if retry_state.attempt_number >= 1:
        logger.info(
            "Retrying %s: attempt %s ended with: %s",
            retry_state.fn,
            retry_state.attempt_number,
            retry_state.outcome,
        )


def dict_to_file(response: Any, filename: str):
    root_path = Path("data")
    root_path.mkdir(exist_ok=True)
    with open(f"{root_path}/{filename}.json", "w", encoding="utf-8") as json_file:
        json.dump(response.dict(), json_file, ensure_ascii=False, indent=4)


class YApi:
    def __init__(self, api_key: str, channel_ids: List[str]) -> None:
        self.youtube: Resource = build("youtube", "v3", developerKey=api_key)
        self.channel_ids = channel_ids
        self.data_handler = DataHandler()

    @staticmethod
    def get_upload_playlist_id(channel_item: ChannelsItem) -> str:
        return channel_item.content_details.related_playlists.uploads

    @staticmethod
    def get_video_ids_from_response(response: PlaylistItems) -> List[str]:
        items_list: List[PlaylistItemsItem] = response.items
        video_ids: List[str] = [item.content_details.video_id for item in items_list]
        return video_ids

    @retry(
        stop=stop_after_attempt(7),
        wait=wait_fixed(10),
        reraise=True,
        before_sleep=retry_write_log_message,
    )
    def perform_channel_stats(self) -> Channels:
        # Get infos about the channel
        # statistics
        # contentDetails / relatedPlaylists / uploads
        part = [
            # "auditDetails",
            "brandingSettings",
            "contentDetails",
            "contentOwnerDetails",
            "id",
            "localizations",
            "snippet",
            "statistics",
            "status",
            "topicDetails",
        ]
        request: HttpRequest = self.youtube.channels().list(
            part=part, id=self.channel_ids
        )
        response: Dict[str, Any] = request.execute()
        channels = Channels.parse_obj(response)
        return channels

    # @retry(stop=stop_after_attempt(7), wait=wait_fixed(10), reraise=True, before_sleep=retry_write_log_message)
    # def perform_features_channels_list(self, channel_id: str) -> ChannelSections:
    #     # feature_channels
    #     request: HttpRequest = self.youtube.channelSections().list(
    #         part="snippet,id,contentDetails", channelId=channel_id
    #     )
    #     response: Dict[str, Any] = request.execute()
    #     channel_sections = ChannelSections.parse_obj(response)
    #     return channel_sections

    @retry(
        stop=stop_after_attempt(7),
        wait=wait_fixed(10),
        reraise=True,
        before_sleep=retry_write_log_message,
    )
    def get_videos_from_playlist(self, upload_playlist_id: str) -> PlaylistItems:
        # Chet uppload videos
        request: HttpRequest = self.youtube.playlistItems().list(
            part=[
                "contentDetails",
                "id",
                "snippet",
                "status",
            ],
            playlistId=upload_playlist_id,
            maxResults=50,
        )
        response: Dict[str, Any] = request.execute()
        playlist_items = PlaylistItems.parse_obj(response)
        return playlist_items

    @retry(
        stop=stop_after_attempt(7),
        wait=wait_fixed(10),
        reraise=True,
        before_sleep=retry_write_log_message,
    )
    def perform_video_info(self, video_id: str) -> Videos:
        request = self.youtube.videos().list(
            part=[
                "contentDetails",
                # "fileDetails",
                "id",
                "liveStreamingDetails",
                "localizations",
                "player",
                # "processingDetails",
                "recordingDetails",
                "snippet",
                "statistics",
                "status",
                # "suggestions",
                "topicDetails",
            ],
            id=video_id,
        )
        response = request.execute()

        videos = Videos.parse_obj(response)
        return videos

    def perform_request(self) -> None:
        # 1: Get channel stats
        # 2: Extrahiere upload-playlist ID from 1
        # 3: Get reduced video-metadata from 2
        # 4. Get featured-channels
        channels: Channels = self.perform_channel_stats()
        # dict_to_file(channels, "chanels")
        for channel_item in channels.items:
            logger.info(f"Parse channel {channel_item.id}")
            upload_playlist_id: str = self.get_upload_playlist_id(channel_item)
            playlist_items: PlaylistItems = self.get_videos_from_playlist(
                upload_playlist_id
            )
            # dict_to_file(playlist_items, "playlistItems")

            ## channel_sections: ChannelSections = self.perform_features_channels_list(channel_id) ## ???
            ## dict_to_file(channel_sections, "channelSections")

            video_ids: List[str] = self.get_video_ids_from_response(playlist_items)
            video_list: List[Videos] = []
            for video_id in video_ids:
                try:
                    video_list.append(self.perform_video_info(video_id))
                except Exception as exception:  # pylint: disable=broad-exception-caught
                    logger.warning(exception)
                    print(exception)
                    continue

            # dict_to_file(video_list[0], "videos")

            data = Data(
                channel_item=channel_item,
                playlist_items=playlist_items,
                video_list=video_list,
            )
            # dict_to_file(data, channel_id)

            self.data_handler.save_to_json(data)
