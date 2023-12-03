import logging
from typing import List, Optional

from sqlalchemy import create_engine, URL, select
from sqlalchemy import ForeignKey, String, Column, Integer, Float, DateTime, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.helpers.helpers import make_now, make_token
from src.base.models import Base


class UserVideo(Base):
    """ """

    __tablename__ = "usersvideos"

    id_usersvideos: Mapped[int] = mapped_column(
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
    id_video: Mapped[str] = mapped_column(
        String(40),
        nullable=False,
        unique=False,
        # FK
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

    interest: Mapped[float] = mapped_column(
        Float(),
        default=2.5,
        unique=False,
        nullable=False,
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

    def __repr__(self) -> str:
        return f"UserVideo(id_usersvideos {self.id_usersvideos})"
