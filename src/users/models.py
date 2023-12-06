import logging
from typing import List, Optional

from sqlalchemy import create_engine, URL, select
from sqlalchemy import ForeignKey, String, Column, Integer, Float, DateTime, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.helpers.helpers import make_now, make_token
from src.base.models import Base


class User(Base):
    __tablename__ = "users"
    id_user: Mapped[int] = mapped_column(
        Integer(),
        autoincrement=True,
        primary_key=True,
        nullable=False,
        unique=True,
    )
    firstname: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=False,
    )
    lastname: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=False,
    )
    email: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True,
    )
    password: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=False,
    )
    token: Mapped[str] = mapped_column(
        String(20),
        default=make_token(),
        nullable=False,
        unique=True,
    )
    sex: Mapped[str] = mapped_column(
        String(1),
        nullable=False,
        unique=False,
        default="-",
    )
    birthdate: Mapped[str] = mapped_column(
        Date(),
        default="1900-01-01",
        nullable=False,
        unique=False,
    )
    is_active: Mapped[int] = mapped_column(
        Integer(),
        default=1,
        nullable=False,
        unique=False,
    )
    is_admin: Mapped[int] = mapped_column(
        Integer(), default=0, nullable=False, unique=False
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
        return f"Users(id_user={self.id_user}, firstname={self.firstname}, lastname={self.lastname}, email={self.email}, password={self.password}, token={self.token}, birthdate={self.birthdate}, is_active={self.is_active}, is_admin={self.is_admin}, created_at={self.created_at})"
