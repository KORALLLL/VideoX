import uvicorn
from fastapi import (
    FastAPI,
    File,
    HTTPException,
    UploadFile,
    status
)
from sqlalchemy import (
    and_,
    exists,
    select
)

from src.config import cfg
from src.db import create_database
from src.dependencies import DatabaseDependencies
from src.models import (
    Video,
    VideoJson,
    VideosModelsProcessed
)
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
    _: VideosModelsProcessed
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
        json_callback_url=f"{cfg.app.bind_addr}/api/v1/video"
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
    pass


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
        host=cfg.app.bind_host,
        port=cfg.app.bind_port,
        reload=True,
    )


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
