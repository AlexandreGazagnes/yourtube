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


class Status(Base):
    __tablename__ = "status"

    id_status: Mapped[str] = mapped_column(primary_key=True)

    def __repr__(self) -> str:
        return f"Status(id_status={self.id_status}"