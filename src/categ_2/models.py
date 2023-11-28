from typing import List
from typing import Optional

from sqlalchemy import create_engine, URL, select
from sqlalchemy import ForeignKey, String, Column, Integer, Float, DateTime, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session


from src.models.base import Base


class Categ2(Base):
    __tablename__ = "categ_2"

    id_categ_2: Mapped[str] = mapped_column(
        String(12),
        primary_key=True,
        nullable=False,
        unique=True,
    )

    def __repr__(self) -> str:
        return f"Categ2(id_categ_2={self.id_categ_2}"

