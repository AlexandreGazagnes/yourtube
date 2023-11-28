import logging
from typing import List, Optional

from sqlalchemy import create_engine, URL, select
from sqlalchemy import ForeignKey, String, Column, Integer, Float, DateTime, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.helpers.helpers import make_now, make_token
from src.base.models import Base


class Channels(Base):
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
