import uvicorn
from fastapi import FastAPI

from app.api.server import Server


def create_app(_=None) -> FastAPI:
    """Create app FastAPI"""

    app = FastAPI()

    return Server(app).get_app()


if __name__ == "__main__":
    uvicorn.run(
        app=create_app(),
        port=8000,
        host="127.0.0.1",
    )
