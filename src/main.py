import uvicorn
from fastapi import FastAPI

from src.db import create_database
from src.models import Video

app = FastAPI()


@app.get("/ping")
async def get_index() -> str:
    return "pong"


async def upload_video():
    xd: Video


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
