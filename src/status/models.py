from typing import List
from typing import Optional

from sqlalchemy import create_engine, URL, select
from sqlalchemy import ForeignKey, String, Column, Integer, Float, DateTime, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session

from src.models.base import Base


class Status(Base):
    __tablename__ = "status"

    id_status: Mapped[str] = mapped_column(
        String(12),
        primary_key=True,
        nullable=False,
        unique=True,
    )

    def __repr__(self) -> str:
        return f"Status(id_status={self.id_status}"

