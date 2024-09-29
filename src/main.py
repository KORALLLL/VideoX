from datetime import datetime
from uuid import uuid4

import uvicorn
import io
from fastapi import FastAPI, File, HTTPException, UploadFile, status
from sqlalchemy import and_, exists, select, update

from src.config import cfg
from src.db import create_database
from src.dependencies import DatabaseDependencies
from src.utils import get_first_frame_from_binary
from src.models import Status, Video, VideoJson, VideosModelsProcessed
from src.s3 import s3
from src.schemas import (
    GetAllVideosResponseSchema,
    GetVideoByIDResponse,
    PollingResponse,
    UploadVideoResponse,
    VideoInGetAllVideosResponse,
)

app = FastAPI()


@app.get("/ping")
async def handle_ping() -> str:
    return "pong"


@app.get("/api/v1/poll/{model_name}")
async def handle_polling(
    db: DatabaseDependencies,
    model_name: str,
) -> PollingResponse:
    subquery = (
        select(VideosModelsProcessed)
        .where(
            and_(
                VideosModelsProcessed.id == Video.id,
                VideosModelsProcessed.model == model_name,
            )
        )
        .exists()
    )
    executed = await db.execute(
        select(Video).where(~subquery).order_by(Video.id).limit(1)
    )
    result: Video | None = executed.scalar_one_or_none()
    if result is None:
        raise HTTPException(
            detail="no new videos", status_code=status.HTTP_404_NOT_FOUND
        )
    return PollingResponse(
        video_url=result.original_video_link,
        video_callback_url=f"{cfg.app.bind_addr}/api/v1/video/"
        f"{result.id}/upload/video",
        json_callback_url=f"{cfg.app.bind_addr}/api/v1/video/"
        f"{result.id}/upload/json",
    )


@app.get("/api/v1/video")
async def handle_get_all_videos(
    db: DatabaseDependencies,
) -> GetAllVideosResponseSchema:
    stmt = select(Video).order_by(Video.id.desc())
    result = await db.execute(stmt)
    videos: list[Video] = result.scalars().all()
    result = GetAllVideosResponseSchema(
        count=len(videos),
        result=[
            VideoInGetAllVideosResponse(
                id=x.id,
                name=x.name,
                created_at=x.created_at,
                image_url=x.original_video_link,
                status=x.status,
            )
            for x in videos
        ],
    )
    return result


@app.get("/api/v1/video/{video_id}")
async def handle_get_video_by_id(
    db: DatabaseDependencies,
    video_id: int,
) -> GetVideoByIDResponse:
    stmt = select(Video).where(Video.id == video_id)  # type: ignore
    result = await db.execute(stmt)
    video: Video | None = result.scalar_one_or_none()
    if video is None:
        raise HTTPException(
            detail="no video with provided id",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    related_jsons = select(VideoJson).where(
        VideoJson.video_id == video.id,  # type: ignore
    )
    result = await db.execute(related_jsons)
    jsons: list[VideoJson] = result.scalars().all()
    max_processed_time = None
    processed = {}
    for json in jsons:
        if (
            max_processed_time is None
            or json.processed_at > max_processed_time
        ):
            max_processed_time = json.processed_at
        processed[json.model_name] = json.processed_json
    response = GetVideoByIDResponse(
        processed_video_url=video.processed_video_link,
        processed_at=max_processed_time,
        id=video.id,
        name=video.name,
        status=video.status,
        uploaded_at=video.uploaded_at,
        original_video_url=video.original_video_link,
        processed=processed,
    )
    return response


@app.post("/api/v1/video")
async def handle_upload_video(
    db: DatabaseDependencies,
    name: str,
    video: UploadFile = File(...),
) -> UploadVideoResponse:
    now = datetime.utcnow()
    video_location = f"videos/{uuid4()}_{video.filename}"
    preview_location = f"videos/preview_{uuid4()}_{video.filename}.jpg"
    video_bytes = await video.read()
    video_file_like = io.BytesIO(video_bytes)
    preview = get_first_frame_from_binary(video_bytes)
    s3.upload_file(video_file_like, video_location)
    s3.upload_file(io.BytesIO(preview), preview_location)
    created_video = Video(
        name=name,
        status=Status.UPLOADED,
        created_at=now,
        uploaded_at=now,
        original_video_path=video_location,
        original_preview_path=preview_location,
    )
    db.add(created_video)
    await db.commit()
    await db.refresh(created_video)

    return UploadVideoResponse(
        id=created_video.id,
        name=created_video.name,
        status=created_video.status,
        created_at=created_video.created_at,
        uploaded_at=created_video.uploaded_at,
        original_video_path=created_video.original_video_path,
        processed_video_path=created_video.processed_video_path,
        original_video_link=created_video.original_video_link,
        processed_video_link=created_video.processed_video_link,
        original_preview_path=created_video.original_preview_path,
        preview_link=created_video.preview_link,
    )


@app.post("/api/v1/video/{video_id}/upload/video")
async def handle_upload_resulted_video(
    db: DatabaseDependencies,
    video_id: int,
    video: UploadFile = File(...),
) -> str:
    now = datetime.utcnow()
    not_found = HTTPException(
        detail="not found",
        status_code=status.HTTP_404_NOT_FOUND,
    )
    res = await db.execute(
        select(Video).where(Video.id == video_id),  # type: ignore
    )
    video_from_db = res.scalar_one_or_none()
    if video_from_db is None:
        raise not_found
    video_location = f"processed/{uuid4()}_{video.filename}"
    stmt = (
        update(Video)
        .values(
            processed_video_path=video_location,
            status=Status.PROCESSED,
        )
        .where(Video.id == video_id)  # type: ignore
    )
    s3.upload_file(video.file, video_location)
    await db.execute(stmt)
    db.add(VideosModelsProcessed(video_id, "video", now))
    await db.commit()

    return s3.generate_link(cfg.s3.aws_bucket, video_location)


@app.post("/api/v1/video/{video_id}/upload/json/{model_name}")
async def handle_upload_json_result(
    db: DatabaseDependencies,
    video_id: int,
    model_name: str,
    json: dict,
) -> None:
    stmt = select(exists(VideoJson)).where(
        VideoJson.video_id == video_id,  # type: ignore
        VideoJson.model_name == model_name,  # type: ignore
    )
    res = await db.execute(stmt)
    result: bool = res.scalar_one_or_none()
    if result:
        raise HTTPException(
            detail="json result already exists",
            status_code=status.HTTP_409_CONFLICT,
        )

    uploaded = VideoJson(
        video_id=video_id,
        model_name=model_name,
        processed_json=json,
    )
    db.add(uploaded)
    await db.commit()
    db.add(
        VideosModelsProcessed(
            id=video_id,
            model=model_name,
        )
    )
    await db.commit()


async def main():
    await create_database()
    uvicorn.run(
        app="src:app",
        host=cfg.app.bind_host,
        port=cfg.app.bind_port,
        reload=True,
    )


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
