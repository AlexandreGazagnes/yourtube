# from typing import List
# from typing import Optional

from sqlalchemy import create_engine, URL, select
from sqlalchemy.orm import Session

# from sqlalchemy import ForeignKey, String, Column, Integer, Float, DateTime, Date
# from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session

# from sqlalchemy import
# from sqlalchemy import DateTime

# from sqlalchemy.orm import Mapped
# from sqlalchemy.orm import mapped_column
# from sqlalchemy.orm import relationship
# from sqlalchemy.orm import Session
from dotenv import load_dotenv

import logging
import pandas as pd

from src.params import get_params
import os

# import psycopg2

params = get_params(os.getenv("MODE", "dev"))

url_object = URL.create(
    drivername="postgresql",
    username=params.get("POSTGRES_USER"),
    password=params.get("POSTGRES_PASSWORD"),  # plain (unescaped) text
    host=params.get("POSTGRES_HOST"),
    database=params.get("POSTGRES_DB"),
    port=params.get("POSTGRES_PORT"),
)


engine = create_engine(url_object)
session = Session(engine)


from src.models.base import Base
from src.models.categ_1 import Categ1
from src.models.categ_2 import Categ2
from src.models.channels import Channels
from src.models.languages import Language
from src.models.videos import Videos
from src.models.status import Status
from src.models.users import Users
from src.models.userschannels import UsersChannels


def _create_all():
    """Create all tables in the engine"""

    # from src.models.base import Base
    # from src.models.categ_1 import Categ1
    # from src.models.categ_2 import Categ2
    # from src.models.channels import Channels
    # from src.models.languages import Language
    # from src.models.videos import Videos
    # from src.models.status import Status
    # from src.models.users import Users
    # from src.models.userschannels import UsersChannels

    Base.metadata.create_all(engine)


def _drop_all():
    """Drop all tables in the engine"""

    # from src.models.base import Base
    # from src.models.categ_1 import Categ1
    # from src.models.categ_2 import Categ2
    # from src.models.channels import Channels
    # from src.models.languages import Language
    # from src.models.videos import Videos
    # from src.models.status import Status
    # from src.models.users import Users
    # from src.models.userschannels import UsersChannels

    Base.metadata.drop_all(engine)


def _boot():
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


def _reboot():
    """ """

    # from src.models.base import Base
    # from src.models.categ_1 import Categ1
    # from src.models.categ_2 import Categ2
    # from src.models.channels import Channels
    # from src.models.languages import Language
    # from src.models.videos import Videos
    # from src.models.status import Status
    # from src.models.users import Users
    # from src.models.userschannels import UsersChannels

    Base.metadata.drop_all(engine)

    _drop_all()
    _create_all()
    _boot()


class Db:
    """Db class to manage the database"""

    users = Users
    userschannels = UsersChannels
    categ_1 = Categ1
    categ_2 = Categ2
    channels = Channels
    languages = Language
    language = Language
    videos = Videos
    engine = engine
    session = session
    create_all = _create_all
    drop_all = _drop_all
    boot = _boot
    reboot = _reboot
