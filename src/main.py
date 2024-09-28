import uvicorn
from datetime import datetime
from fastapi import FastAPI, File, HTTPException, UploadFile, status
from sqlalchemy import exists, select, func
from src.config import cfg
from src.db import create_database
from src.s3 import s3
from src.dependencies import DatabaseDependencies
from src.models import VideoJson, Video, Status
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
    pass


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
    stmt = select(func.max(Video.id))
    id = await db.execute(stmt)
    id: int | None = id.scalar_one_or_none()
    id = id + 1 if id else 1

    video_location = f"videos/{id}_{name}"
    s3.upload_file(video.file, video_location)
    now = datetime.utcnow()

    created_video = Video(
        id=id,
        name=name,
        status=Status.UPLOADED,
        created_at=now,
        uploaded_at=now,
        original_video_path=video_location,
    )
    await db.add(created_video)
    await db.commit
    stmt = select(Video).where(id=created_video.id)
    created_video = await db.execute(stmt)
    created_video: Video = created_video.scalar()
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
    await db.commit()


async def main():
    await create_database()
    uvicorn.run(
        app="src:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
