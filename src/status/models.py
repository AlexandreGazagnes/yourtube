import logging
from typing import List, Optional

from sqlalchemy import create_engine, URL, select
from sqlalchemy import ForeignKey, String, Column, Integer, Float, DateTime, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.helpers.helpers import make_now, make_token
from src.base.models import Base


class Status(Base):
    __tablename__ = "status"

    id_status: Mapped[str] = mapped_column(
        String(12),
        primary_key=True,
        nullable=False,
        unique=True,
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

    def __repr__(self) -> str:
        return f"Status(id_status={self.id_status}"
