import logging
from typing import List, Optional

from sqlalchemy import create_engine, URL, select
from sqlalchemy import ForeignKey, String, Column, Integer, Float, DateTime, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.helpers.helpers import make_now, make_token
from src.base.models import Base


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
        String(50),
        unique=False,
        nullable=False,
    )
    interest: Mapped[float] = mapped_column(
        Float(),
        default=2.5,
        unique=False,
        nullable=False,
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
    thumbnail_url: Mapped[str] = mapped_column(
        String(300),
        default="https://i.ytimg.com/vi/kJQP7kiw5Fk/hqdefault.jpg?sqp=-oaymwEcCPYBEIoBSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLC7mQvF1DbgLkymd5TjUQjWLbaJ3A",
        nullable=False,
        unique=False,
    )
    keywords: Mapped[str] = mapped_column(
        String(120),
        default="None",
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
