from functools import wraps

import validators
from fastapi import HTTPException, status


def validator_url(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        print(args[2])
        if not validators.url(args[2].target_url):
            HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid URL",
            )
        else:
            return await func(*args, **kwargs)

    return wrapper
