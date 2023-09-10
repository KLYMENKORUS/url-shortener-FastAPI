from .routers import Routers
from api import router

__routers__: Routers = Routers(routers=(router,))
