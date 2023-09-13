from sqlalchemy import String, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, ModelWithUUID, ModelWithTime


class URL(Base, ModelWithUUID, ModelWithTime):
    key: Mapped[str] = mapped_column(
        String,
        unique=True,
        index=True,
        nullable=False,
    )
    target_url: Mapped[str] = mapped_column(
        String,
        index=True,
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )
    clicks: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )
