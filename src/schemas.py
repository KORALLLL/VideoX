from datetime import datetime

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


class VideoInGetAllVideosResponse(BaseModel):
    id: int
    name: str
    created_at: datetime
    image_url: str


class GetAllVideosResponseSchema(BaseModel):
    count: int
    result: list[VideoInGetAllVideosResponse]


class PollingResponse(BaseModel):
    video_url: str
    video_callback_url: str
    json_callback_url: str


class UploadVideoResponse(BaseModel):
    pass
