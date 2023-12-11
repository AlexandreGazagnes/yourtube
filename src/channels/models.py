import logging
from typing import List, Optional

from sqlalchemy import create_engine, URL, select
from sqlalchemy import ForeignKey, String, Column, Integer, Float, DateTime, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.helpers.helpers import make_now, make_token
from src.base.models import Base


DEFAULT_THUMBNAIL_CHANNEL_URL = "https://i.ytimg.com/vi/kJQP7kiw5Fk/hqdefault.jpg?sqp=-oaymwEcCPYBEIoBSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLC7mQvF1DbgLkymd5TjUQjWLbaJ3A"

LOREM = """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore
magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur 
sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."""


class Channel(Base):
    """Channels model"""

    __tablename__ = "channels"

    id_channel: Mapped[str] = mapped_column(
        String(40),
        primary_key=True,
        nullable=False,
        unique=True,
    )

    name: Mapped[str] = mapped_column(
        String(70),
        unique=False,
        nullable=False,
    )

    author: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=False,
    )

    # interest: Mapped[float] = mapped_column(
    #     Float(),
    #     default=2.5,
    #     unique=False,
    #     nullable=False,
    # )

    youtube_subscribers: Mapped[int] = mapped_column(
        Integer(),
        default=0,
        nullable=False,
        unique=False,
    )

    yourtube_subscribers: Mapped[int] = mapped_column(
        Integer(),
        default=0,
        nullable=False,
        unique=False,
    )

    created_at: Mapped[str] = mapped_column(
        DateTime(),
        default=make_now(),
        unique=False,
        nullable=False,
    )

    updated_at: Mapped[str] = mapped_column(
        DateTime(),
        default=make_now(),
        unique=False,
        nullable=False,
    )

    thumbnail_channel_url: Mapped[str] = mapped_column(
        String(300),
        default=DEFAULT_THUMBNAIL_CHANNEL_URL,
        nullable=False,
        unique=False,
    )

    keywords: Mapped[str] = mapped_column(
        String(120),
        default="None",
        nullable=False,
        unique=False,
    )

    channel_description: Mapped[str] = mapped_column(
        String(500),
        default=LOREM,
        nullable=False,
        unique=False,
    )

    id_language: Mapped[str] = mapped_column(
        String(12),
        default="?",
        unique=False,
        nullable=False,
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
        return f"Channels(id_channel={self.id_channel}, name={self.name}, id_categ_1={self.id_categ_1}"

    def to_dict(self):
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}
