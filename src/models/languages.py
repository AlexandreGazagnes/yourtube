from typing import List
from typing import Optional

from sqlalchemy import create_engine, URL, select
from sqlalchemy import ForeignKey, String, Column, Integer, Float, DateTime, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session


class Base(DeclarativeBase):
    pass
    # def serialize(self):
    #     # return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    #     return self.__dict__


class Language(Base):
    __tablename__ = "language"
    id_language: Mapped[str] = mapped_column(
        String(12),
        primary_key=True,
        nullable=False,
        unique=True,
    )

    def __repr__(self) -> str:
        return f"Language(id_language={self.id_language}"
