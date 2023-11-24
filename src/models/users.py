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


class Users(Base):
    __tablename__ = "users"
    id_user: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, nullable=False
    )
    firstname: Mapped[str] = mapped_column()
    lastname: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column()
    password: Mapped[str] = mapped_column()
    token: Mapped[str] = mapped_column(default=make_token(), nullable=False)
    birthdate: Mapped[str] = mapped_column()
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    is_admin: Mapped[bool] = mapped_column(default=False, nullable=False)
    created_at: Mapped[str] = mapped_column(default=make_now(), nullable=False)

    def __repr__(self) -> str:
        return f"Users(id_user={self.id_user}, firstname={self.firstname}, lastname={self.lastname}, email={self.email}, password={self.password}, token={self.token}, birthdate={self.birthdate}, is_active={self.is_active}, is_admin={self.is_admin}, created_at={self.created_at})"
