import uvicorn
from fastapi import (
    FastAPI,
    File,
    UploadFile
)

from src.db import create_database
from src.dependencies import DatabaseDependencies
from src.models import Video
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


@app.get("/api/v1/poll")
async def handle_polling(
    db: DatabaseDependencies,
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


async def upload_video():
    _: Video


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
