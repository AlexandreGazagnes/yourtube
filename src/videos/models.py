import logging
from typing import List, Optional

from sqlalchemy import create_engine, URL, select
from sqlalchemy import ForeignKey, String, Column, Integer, Float, DateTime, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.helpers.helpers import make_now, make_token
from src.base.models import Base


DEFAULT_THUMBNAIL_VIDEO_URL = "https://i.ytimg.com/vi/kJQP7kiw5Fk/hqdefault.jpg?sqp=-oaymwEcCPYBEIoBSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLC7mQvF1DbgLkymd5TjUQjWLbaJ3A"
DEFAULT_DURATION = 360


LOREM = """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore
magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur 
sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."""


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

    id_categ_0: Mapped[str] = mapped_column(
        String(12),
        default="?",
        unique=False,
        nullable=False,
        # FK
    )

    video_description: Mapped[str] = mapped_column(
        String(500),
        default=LOREM,
        nullable=False,
        unique=False,
    )

    def __repr__(self) -> str:
        return f"Videos(id_video={self.id_video}, title={self.title}, author={self.author}, published={self.published}, stars={self.stars}, views={self.views}, id_channel={self.id_channel})"

    def to_dict(self):
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}
