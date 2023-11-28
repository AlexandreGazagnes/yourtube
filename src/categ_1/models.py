from typing import List, Optional

from sqlalchemy import create_engine, URL, select
from sqlalchemy import (
    ForeignKey,
    String,
    Column,
    Integer,
    Float,
    DateTime,
    Date,
    Boolean,
)

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session

from src.base.models import Base


class Categ1(Base):
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

    def __repr__(self) -> str:
        return f"Categ1(id_categ_1={self.id_categ_1}, id_categ_2={self.id_categ_2}"
