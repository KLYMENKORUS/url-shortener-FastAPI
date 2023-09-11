import uuid
from datetime import datetime

from sqlalchemy import text, func, DateTime
from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.dialects.postgresql import UUID


class Base(DeclarativeBase):
    __abstract__: bool = True

    @declared_attr
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    def __repr__(self) -> str:
        params = "".join(
            f"{attr}={value!r}"
            for attr, value in self.__dict__.items()
            if not value.startswith("_")
        )
        return f"{type(self.__name__)}{(params)}"


class ModelWithUUID:
    """BaseUUID model class that represents ID with an UUID type"""

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
        index=True,
        nullable=False,
    )


class ModelWithTime:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
