from typing import Any
import secrets
import string


class CreateRandomKey:
    def __init__(self, length: int = 6) -> None:
        self.length = length

    def __call__(self) -> Any:
        return self._random_key()

    def _random_key(self) -> str:
        chars = string.ascii_uppercase + string.digits
        return "".join(secrets.choice(chars) for _ in range(self.length))
