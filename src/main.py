import uvicorn
from fastapi import (
    FastAPI,
    File,
    HTTPException,
    UploadFile,
    status
)
from sqlalchemy import (
    exists,
    select
)

from src.db import create_database
from src.dependencies import DatabaseDependencies
from src.models import VideoJson
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
        host="0.0.0.0",
        port=8000,
        reload=True,
    )


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
