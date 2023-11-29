import logging
from typing import List, Optional

from sqlalchemy import create_engine, URL, select
from sqlalchemy import ForeignKey, String, Column, Integer, Float, DateTime, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.helpers.helpers import make_now, make_token
from src.base.models import Base


class Categ1(Base):
    """Categ1 model"""

    __tablename__ = "categ_1"

    id_categ_1: Mapped[str] = mapped_column(
        String(12),
        primary_key=True,
        nullable=False,
        unique=True,
    )

    id_categ_2: Mapped[str] = mapped_column(
        String(12),
        default="Misc.",
        unique=False,
        nullable=False,
        # FK
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
        return f"Categ1(id_categ_1={self.id_categ_1}, id_categ_2={self.id_categ_2}"
