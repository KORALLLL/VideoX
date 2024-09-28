import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/ping")
async def get_index() -> str:
    return "pong"


def main():
    uvicorn.run(
        app="src:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )


if __name__ == "__main__":
    main()
