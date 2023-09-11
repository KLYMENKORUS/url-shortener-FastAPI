from typing import ClassVar, Type

from fastapi import FastAPI

from app.api.core import __routers__


class Server:
    __app: ClassVar[Type[FastAPI]]

    def __init__(self, app: FastAPI):
        self.__app = app
        self.__register_routes(app)

    def get_app(self) -> FastAPI:
        return self.__app

    @staticmethod
    def __register_routes(app: FastAPI):
        __routers__.register_routers(app)
