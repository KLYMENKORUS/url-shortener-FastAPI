from dataclasses import dataclass
from fastapi import FastAPI, APIRouter


@dataclass(frozen=True)
class Routers:
    routers: tuple[APIRouter, ...]

    def register_routers(self, app: FastAPI) -> None:
        """Register routes"""
        for router in self.routers:
            app.include_router(router)
