from typing import List
from typing import Optional

from sqlalchemy import create_engine, URL, select
from sqlalchemy import ForeignKey, String, Column, Integer, Float, DateTime, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session

from src.helpers import make_now, make_token

from src.models.base import Base


class Videos(Base):
    __tablename__ = "videos"
    id_video: Mapped[str] = mapped_column(
        String(40),
        primary_key=True,
        nullable=False,
        unique=True,
    )
    title: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=False,
    )
    author: Mapped[str] = mapped_column(
        String(50),
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
    stars: Mapped[float] = mapped_column(
        Float(),
        default=0,
        nullable=False,
        unique=False,
    )
    views: Mapped[int] = mapped_column(
        Integer(),
        default=0,
        nullable=False,
        unique=False,
    )
    watched: Mapped[int] = mapped_column(
        Integer(),
        default=0,
        nullable=False,
        unique=False,
    )
    id_status: Mapped[str] = mapped_column(
        String(12),
        default="none",
        nullable=False,
        unique=False,
        # FK
    )
    id_channel: Mapped[str] = mapped_column(
        String(40),
        nullable=False,
        unique=False,
        # FK
    )

    def __repr__(self) -> str:
        return f"Videos(id_video={self.id_video}, title={self.title}, author={self.author}, published={self.published}, stars={self.stars}, views={self.views}, id_channel={self.id_channel}"
