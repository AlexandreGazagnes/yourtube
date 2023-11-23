from typing import List
from typing import Optional

from sqlalchemy import create_engine, URL, select
from sqlalchemy import ForeignKey, String, Column, Integer, Float, DateTime, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session

# from sqlalchemy import
# from sqlalchemy import DateTime

# from sqlalchemy.orm import Mapped
# from sqlalchemy.orm import mapped_column
# from sqlalchemy.orm import relationship
# from sqlalchemy.orm import Session


url_object = URL.create(
    drivername="mysql+mysqlconnector",
    username="root",
    password="password",  # plain (unescaped) text
    host="localhost",
    database="yourdb",
)


engine = create_engine(url_object)
session = Session(engine)


class Base(DeclarativeBase):
    def serialize(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Language(Base):
    __tablename__ = "language"
    id_language: Mapped[str] = mapped_column(primary_key=True)

    def __repr__(self) -> str:
        return f"Language(id_language={self.id_language}"


class Categ2(Base):
    __tablename__ = "categ_2"
    id_categ_2: Mapped[str] = mapped_column(primary_key=True)

    def __repr__(self) -> str:
        return f"Categ2(id_categ_2={self.id_categ_2}"


class Categ1(Base):
    __tablename__ = "categ_1"
    id_categ_1: Mapped[str] = mapped_column(primary_key=True)
    id_categ_2: Mapped[str] = mapped_column()

    def __repr__(self) -> str:
        return f"Categ1(id_categ_1={self.id_categ_1}, id_categ_2={self.id_categ_2}"


class Channels(Base):
    __tablename__ = "channels"
    id_channel: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    interest: Mapped[float] = mapped_column()
    date: Mapped[str] = mapped_column()
    id_language: Mapped[str] = mapped_column()
    id_categ_1: Mapped[str] = mapped_column()
    id_language: Mapped[str] = mapped_column()

    def __repr__(self) -> str:
        return f"Channels(id_channel={self.id_channel}, name={self.name}, id_categ_1={self.id_categ_1}"


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
