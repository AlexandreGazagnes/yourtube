from typing import List
from typing import Optional

from sqlalchemy import create_engine, URL, select
from sqlalchemy import ForeignKey, String, Column, Integer, Float, DateTime, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session
from src.helpers import make_now, make_token


from src.models.base import Base


class UsersChannels(Base):
    __tablename__ = "userschannels"
    id_userschannels: Mapped[int] = mapped_column(
        Integer(),
        primary_key=True,
        autoincrement=True,
        nullable=False,
        unique=True,
    )
    id_user: Mapped[int] = mapped_column(
        Integer(),
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
        return f"UsersChannels(id_userschannels={self.id_userschannels}, id_user={self.id_user}, id_channel={self.id_channel})"

