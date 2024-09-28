from datetime import datetime
from enum import Enum
from typing import Any

from sqlalchemy import DateTime, ForeignKey, Integer, Sequence
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column

from src.config import cfg
from src.db import Base
from src.s3 import s3

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

    @hybrid_property
    def original_video_link(self):
        if self.original_video_path not in (None, ""):
            return s3.generate_link(
                bucket=cfg.s3.aws_bucket,
                key=self.original_video_path,
            )
        return ""

    @hybrid_property
    def processed_video_link(self):
        if self.processed_video_path not in (None, ""):
            return s3.generate_link(
                bucket=cfg.s3.aws_bucket,
                key=self.processed_video_path,
            )
        return ""


class VideosModelsProcessed(Base):
    __tablename__ = "video_model_processed"

    id: Mapped[int] = mapped_column(primary_key=True)
    model: Mapped[str] = mapped_column(primary_key=True)
    processed_at: Mapped[datetime | None]


class VideoJson(Base):
    __tablename__ = "videos_json"

    video_id: Mapped[int] = mapped_column(
        ForeignKey(
            "videos.id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        primary_key=True,
    )
    model_name: Mapped[str] = mapped_column(primary_key=True)
    processed_json: Mapped[Any] = mapped_column(
        JSONB,
    )
    processed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
    )
