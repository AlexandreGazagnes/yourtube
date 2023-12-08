import logging
from typing import List, Optional

from sqlalchemy import create_engine, URL, select
from sqlalchemy import ForeignKey, String, Column, Integer, Float, DateTime, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.helpers.helpers import make_now, make_token
from src.base.models import Base


class UserChannel(Base):
    """ """

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
    interest: Mapped[float] = mapped_column(
        Float(),
        default=2.5,
        unique=False,
        nullable=False,
    )

    created_at: Mapped[str] = mapped_column(
        DateTime(),
        default=make_now(),
        nullable=False,
        unique=False,
    )
    updated_at: Mapped[str] = mapped_column(
        DateTime(),
        default=make_now(),
        nullable=False,
        unique=False,
    )

    enable_shorts: Mapped[int] = mapped_column(
        Integer(),
        default=0,
        nullable=False,
        unique=False,
    )

    def __repr__(self) -> str:
        return f"UsersChannels(id_userschannels={self.id_userschannels}, id_user={self.id_user}, id_channel={self.id_channel})"
