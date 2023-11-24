from typing import List
from typing import Optional

from sqlalchemy import create_engine, URL, select
from sqlalchemy import ForeignKey, String, Column, Integer, Float, DateTime, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session
from src.helpers import make_now, make_token


class Base(DeclarativeBase):
    pass
    # def serialize(self):
    #     # return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    #     return self.__dict__


class UsersChannels(Base):
    __tablename__ = "userschannels"
    id_userschannels: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, nullable=False
    )
    id_user: Mapped[int] = mapped_column()
    id_channel: Mapped[str] = mapped_column()

    def __repr__(self) -> str:
        return f"UsersChannels(id_userschannels={self.id_userschannels}, id_user={self.id_user}, id_channel={self.id_channel})"
