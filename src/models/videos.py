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


class Videos(Base):
    __tablename__ = "videos"
    id_video: Mapped[str] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    author: Mapped[str] = mapped_column()
    published: Mapped[str] = mapped_column()
    stars: Mapped[float] = mapped_column()
    views: Mapped[int] = mapped_column()
    id_channel: Mapped[str] = mapped_column()

    def __repr__(self) -> str:
        return f"Videos(id_video={self.id_video}, title={self.title}, author={self.author}, published={self.published}, stars={self.stars}, views={self.views}, id_channel={self.id_channel}"
