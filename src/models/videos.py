from typing import List
from typing import Optional

from sqlalchemy import create_engine, URL, select
from sqlalchemy import ForeignKey, String, Column, Integer, Float, DateTime, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session

from src.helpers import make_now, make_token

from src.models.base import Base


class Videos(Base):
    __tablename__ = "videos"
    id_video: Mapped[str] = mapped_column(primary_key=True, nullable=False, unique=True)
    title: Mapped[str] = mapped_column(nullable=False)
    author: Mapped[str] = mapped_column(nullable=False)
    published: Mapped[str] = mapped_column(default=make_now(), nullable=False)
    stars: Mapped[float] = mapped_column(default=0, nullable=False)
    views: Mapped[int] = mapped_column(default=0, nullable=False)
    id_channel: Mapped[str] = mapped_column(nullable=False)
    watched: Mapped[int] = mapped_column(default=0, nullable=False)
    id_status: Mapped[str] = mapped_column(default="none", nullable=False)

    def __repr__(self) -> str:
        return f"Videos(id_video={self.id_video}, title={self.title}, author={self.author}, published={self.published}, stars={self.stars}, views={self.views}, id_channel={self.id_channel}"
