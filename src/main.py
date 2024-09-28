import uvicorn
from uuid import uuid4
from datetime import datetime
from fastapi import FastAPI, File, HTTPException, UploadFile, status
from sqlalchemy import and_, exists, select, func

from src.config import cfg
from src.db import create_database
from src.s3 import s3
from src.dependencies import DatabaseDependencies
from src.models import Video, VideoJson, VideosModelsProcessed, Status
from src.schemas import (
    GetAllVideosResponseSchema,
    GetVideoByIDResponse,
    PollingResponse,
    UploadVideoResponse,
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
    pass


@app.get("/api/v1/video/{video_id}")
async def handle_get_video_by_id(
    db: DatabaseDependencies,
    video_id: int,
) -> GetVideoByIDResponse:
    pass


@app.post("/api/v1/video")
async def handle_upload_video(
    db: DatabaseDependencies,
    name: str,
    video: UploadFile = File(...),
) -> UploadVideoResponse:
    now = datetime.utcnow()
    video_location = f"videos/{uuid4()}_{video.filename}"
    created_video = Video(
        name=name,
        status=Status.UPLOADED,
        created_at=now,
        uploaded_at=now,
        original_video_path=video_location,
    )
    db.add(created_video)
    await db.commit()
    await db.refresh(created_video)

    s3.upload_file(video.file, video_location)

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
    )


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
