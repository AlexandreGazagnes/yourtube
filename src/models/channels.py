from typing import List
from typing import Optional

from sqlalchemy import create_engine, URL, select
from sqlalchemy import ForeignKey, String, Column, Integer, Float, DateTime, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session
from src.helpers import make_now, make_token


class Base(DeclarativeBase):
    pass
    # def serialize(self):
    #     # return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    #     return self.__dict__


class Channels(Base):
    __tablename__ = "channels"
    id_channel: Mapped[str] = mapped_column(
        String(30),
        primary_key=True,
        nullable=False,
        unique=True,
    )
    name: Mapped[str] = mapped_column(
        String(30),
        unique=False,
        nullable=False,
    )
    interest: Mapped[float] = mapped_column(
        Float(),
        default=2.5,
        unique=False,
        nullable=False,
    )
    date: Mapped[str] = mapped_column(
        Date(),
        default=make_now(),
        unique=False,
        nullable=False,
    )
    id_language: Mapped[str] = mapped_column(
        String(12),
        default="?",
        unique=False,
        nullable=False,
    )
    id_categ_1: Mapped[str] = mapped_column(
        String(12),
        default="Misc.",
        unique=False,
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"Channels(id_channel={self.id_channel}, name={self.name}, id_categ_1={self.id_categ_1}"
