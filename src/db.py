import logging, os

from typing import List, Optional

from sqlalchemy import create_engine, URL, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session

from dotenv import load_dotenv

import pandas as pd

from src.params import get_params, params

from src.base.models import Base
from src.categ_1.models import Categ1
from src.categ_2.models import Categ2
from src.channels.models import Channel
from src.languages.models import Language
from src.videos.models import Video
from src.status.models import Status
from src.users.models import User
from src.userschannels.models import UserChannel


# class Base(DeclarativeBase):
#     pass
#     # def serialize(self):
#     #     # return {c.name: getattr(self, c.name) for c in self.__table__.columns}
#     #     return self.__dict__


def _get_engine(params: dict = params):
    url_object = URL.create(
        drivername="postgresql",
        username=params.get("POSTGRES_USER"),
        password=params.get("POSTGRES_PASSWORD"),  # plain (unescaped) text
        host=params.get("POSTGRES_HOST"),
        database=params.get("POSTGRES_DB"),
        port=params.get("POSTGRES_PORT"),
    )

    engine = create_engine(url_object)
    return engine


def _get_session(params: dict = params):
    engine = _get_engine(params)
    session = Session(engine)
    return session


engine = _get_engine(params=params)
session = _get_session(params=params)


def _create_all(engine=engine):
    """Create all tables in the engine"""

    Base.metadata.create_all(engine)


def _drop_all(engine=engine):
    """Drop all tables in the engine"""

    Base.metadata.drop_all(engine)


def _boot(engine=engine):
    """ """

    categ_1_df = pd.read_csv("./data/tables/categ_1.csv")
    with Session(engine) as session:
        try:
            for _, row in categ_1_df.iterrows():
                session.add(Categ1(**row.to_dict()))
                session.commit()
        except Exception as e:
            print(e)

    categ_2_df = pd.read_csv("./data/tables/categ_2.csv")
    with Session(engine) as session:
        for _, row in categ_2_df.iterrows():
            session.add(Categ2(**row.to_dict()))
            session.commit()

    channels_df = pd.read_csv("./data/tables/channels.csv")
    with Session(engine) as session:
        for _, row in channels_df.iterrows():
            session.add(Channels(**row.to_dict()))
            session.commit()

    language_df = pd.read_csv("./data/tables/language.csv")
    with Session(engine) as session:
        for _, row in language_df.iterrows():
            session.add(Language(**row.to_dict()))
            session.commit()

    status_df = pd.read_csv("./data/tables/status.csv")
    with Session(engine) as session:
        for _, row in status_df.iterrows():
            session.add(Status(**row.to_dict()))
            session.commit()

    users_df = pd.read_csv("./data/tables/users.csv")
    with Session(engine) as session:
        for _, row in users_df.iterrows():
            session.add(Users(**row.to_dict()))
            session.commit()

    userschannels_df = pd.read_csv("./data/tables/userschannels.csv")
    with Session(engine) as session:
        for _, row in userschannels_df.iterrows():
            session.add(UsersChannels(**row.to_dict()))
            session.commit()

    videos_df = pd.read_csv("./data/tables/videos.csv")
    with Session(engine) as session:
        for _, row in videos_df.iterrows():
            session.add(Videos(**row.to_dict()))
            session.commit()


def _reboot(engine=engine):
    """ """

    _drop_all(engine=engine)
    _create_all(engine=engine)
    _boot(engine=engine)


class Db:
    """Db class to manage the database"""

    user = User
    userchannel = UserChannel
    categ_1 = Categ1
    categ_2 = Categ2
    channel = Channel
    language = Language
    video = Video
    engine = _get_engine
    session = _get_session
    create_all = _create_all
    drop_all = _drop_all
    boot = _boot
    reboot = _reboot
