from .routers import Routers
from app.api import router

__routers__: Routers = Routers(routers=(router,))
