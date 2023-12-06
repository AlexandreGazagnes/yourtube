import logging
from typing import List, Optional

from sqlalchemy import create_engine, URL, select
from sqlalchemy import ForeignKey, String, Column, Integer, Float, DateTime, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.helpers.helpers import make_now, make_token
from src.base.models import Base


DEFAULT_THUMBNAIL_VIDEO_URL = "https://i.ytimg.com/vi/kJQP7kiw5Fk/hqdefault.jpg?sqp=-oaymwEcCPYBEIoBSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLC7mQvF1DbgLkymd5TjUQjWLbaJ3A"
DEFAULT_DURATION = 360


class Video(Base):
    """ """

    __tablename__ = "videos"

    id_video: Mapped[str] = mapped_column(
        String(40),
        primary_key=True,
        nullable=False,
        unique=True,
    )
    title: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        unique=False,
    )

    category: Mapped[str] = mapped_column(
        String(50),
        default="Misc.",
        nullable=False,
        unique=False,
    )
    keywords: Mapped[str] = mapped_column(
        String(120),
        default="None",
        nullable=False,
        unique=False,
    )
    thumbnail_video_url: Mapped[str] = mapped_column(
        String(300),
        default=DEFAULT_THUMBNAIL_VIDEO_URL,
        nullable=False,
        unique=False,
    )

    published: Mapped[str] = mapped_column(
        DateTime(),
        default=make_now(),
        nullable=False,
        unique=False,
    )

    created_at: Mapped[str] = mapped_column(
        DateTime(),
        default=make_now(),
        nullable=False,
        unique=False,
    )
    updated_at: Mapped[str] = mapped_column(
        DateTime(),
        default=make_now(),
        nullable=False,
        unique=False,
    )
    stars: Mapped[float] = mapped_column(
        Float(),
        default=-1.0,
        nullable=False,
        unique=False,
    )
    duration: Mapped[int] = mapped_column(
        Integer(),
        default=DEFAULT_DURATION,
        nullable=False,
        unique=False,
    )
    votes: Mapped[int] = mapped_column(
        Integer(),
        default=-1,
        nullable=False,
        unique=False,
    )
    views: Mapped[int] = mapped_column(
        Integer(),
        default=-1,
        nullable=False,
        unique=False,
    )

    id_channel: Mapped[str] = mapped_column(
        String(40),
        nullable=False,
        unique=False,
        # FK
    )

    id_categ_1: Mapped[str] = mapped_column(
        String(12),
        default="Misc.",
        unique=False,
        nullable=False,
        # FK
    )

    def __repr__(self) -> str:
        return f"Videos(id_video={self.id_video}, title={self.title}, author={self.author}, published={self.published}, stars={self.stars}, views={self.views}, id_channel={self.id_channel})"
