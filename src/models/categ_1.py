from typing import List
from typing import Optional

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

# from sqlalchemy.orm
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session


from src.models.base import Base

# class Base(DeclarativeBase):
#     pass
#     # def serialize(self):
#     #     # return {c.name: getattr(self, c.name) for c in self.__table__.columns}
#     #     return self.__dict__


class Categ1(Base):
    __tablename__ = "categ_1"

    id_categ_1: Mapped[str] = mapped_column(
        String(12),
        primary_key=True,
        nullable=False,
        unique=True,
    )

    id_categ_2: Mapped[str] = mapped_column(
        String(30),
        default="Misc.",
        unique=False,
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"Categ1(id_categ_1={self.id_categ_1}, id_categ_2={self.id_categ_2}"
