from typing import List

from pydantic import BaseModel

from youtube_analyzer.schema.channels import ChannelsItem
from youtube_analyzer.schema.playlist_items import PlaylistItems
from youtube_analyzer.schema.videos import Videos


class Data(BaseModel):
    channel_item: ChannelsItem
    playlist_items: PlaylistItems
    video_list: List[Videos]
