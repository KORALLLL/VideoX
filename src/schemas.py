from datetime import datetime
from typing import Any, AnyStr

from pydantic import BaseModel

from src.models import Status


class GetVideoByIDResponse(BaseModel):
    id: int
    name: str
    status: Status
    uploaded_at: datetime
    processed_at: datetime | None
    original_video_url: str
    processed_video_url: str | None
    processed: dict[str, Any]


class VideoInGetAllVideosResponse(BaseModel):
    id: int
    name: str
    created_at: datetime
    image_url: str
    status: Status


class GetAllVideosResponseSchema(BaseModel):
    count: int
    result: list[VideoInGetAllVideosResponse]


class PollingResponse(BaseModel):
    video_url: str
    video_callback_url: str
    json_callback_url: str


class UploadVideoResponse(BaseModel):
    id: int
    name: str | None
    status: Status
    created_at: datetime
    uploaded_at: datetime
    original_video_path: str
    processed_video_path: str | None
    original_video_link: str | None
    processed_video_link: str | None
    original_preview_path: str
    preview_link: str
