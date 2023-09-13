from typing import Annotated

from fastapi import Depends

from app.adapters.services.database.core import DatabaseUOW


UOWDepends = Annotated[DatabaseUOW, Depends(DatabaseUOW)]
