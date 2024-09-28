from datetime import datetime
from enum import Enum
from typing import Any

from sqlalchemy import (
    Integer,
    Sequence
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from src.db import Base

TABLE_ID = Sequence("video_ids_sequence", start=100)


class Status(Enum):
    CREATED = "CREATED"
    UPLOADED = "UPLOADED"
    PROCESSING = "PROCESSING"
    PROCESSED = "PROCESSED"


class Video(Base):
    __tablename__ = "videos"

    id: Mapped[int] = mapped_column(
        Integer,
        TABLE_ID,
        primary_key=True,
    )
    name: Mapped[str | None] = mapped_column(
        index=True,
        nullable=True,
    )
    status: Mapped[Status]
    created_at: Mapped[datetime] = mapped_column()
    uploaded_at: Mapped[datetime] = mapped_column()
    original_video_path: Mapped[str]
    processed_video_path: Mapped[str | None]
    processed_json: Mapped[Any | None] = mapped_column(
        JSONB,
        nullable=True,
    )
