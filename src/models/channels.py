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


class Channels(Base):
    __tablename__ = "channels"
    id_channel: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    interest: Mapped[float] = mapped_column()
    date: Mapped[str] = mapped_column()
    id_language: Mapped[str] = mapped_column()
    id_categ_1: Mapped[str] = mapped_column()

    def __repr__(self) -> str:
        return f"Channels(id_channel={self.id_channel}, name={self.name}, id_categ_1={self.id_categ_1}"
