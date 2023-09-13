__all__ = ("load_settings",)

from .settings import load_settings


from .routers import Routers
from app.api.routers.url import router as router_url

__routers__: Routers = Routers(routers=(router_url,))
