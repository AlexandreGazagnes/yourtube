import logging, os, csv

from typing import List, Optional

from sqlalchemy import create_engine, URL, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session

from dotenv import load_dotenv

import pandas as pd
import numpy as np

from src.params import get_params, params

from src.base.models import Base
from src.categ_1.models import Categ1
from src.categ_2.models import Categ2
from src.channels.models import Channel
from src.languages.models import Language
from src.status.models import Status
from src.users.models import User
from src.userschannels.models import UserChannel
from src.usersvideos.models import UserVideo
from src.videos.models import Video


# from src.videos.functions import fix_videos as _fix_videos


# from src.helpers.queries import Query

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

    logging.warning("Creating all tables in the engine")

    Base.metadata.create_all(engine)


def _drop_all(engine=engine):
    """Drop all tables in the engine"""

    logging.warning("Dropping all tables in the engine")

    Base.metadata.drop_all(engine)


def _boot(
    engine=engine,
    N_SPLITS_VIDEOS: int = 30,
    path="./data/tables/",
):
    """ """

    pair_dict = [
        ("categ_1.csv", Categ1),
        ("categ_2.csv", Categ2),
        ("channels.csv", Channel),
        ("languages.csv", Language),
        ("status.csv", Status),
        ("users.csv", User),
        ("userschannels.csv", UserChannel),
        ("usersvideos.csv", UserVideo),
        ("videos.csv", Video),
    ]

    logging.warning("Booting database")

    for fn, Obj in pair_dict:
        # pass videos
        if "videos" in fn:
            continue

        logging.warning(f"{fn}")

        df = pd.read_csv(os.path.join(path, fn))
        with Session(engine) as session:
            try:
                for _, row in df.iterrows():
                    session.add(Obj(**row.to_dict()))
                    session.commit()
            except Exception as e:
                logging.error(f"{e} : {fn} - {row.to_dict()}")

    # special case for videos
    logging.warning("videos")
    videos_df = pd.read_csv("./data/tables/videos.csv")
    # logging.warning(f"{videos_df.head(1).to_dict()}")
    splited_videos_df = np.array_split(videos_df, N_SPLITS_VIDEOS)
    for i, sub_videos_df in enumerate(splited_videos_df):
        with Session(engine) as session:
            for _, row in sub_videos_df.iterrows():
                session.add(Video(**row.to_dict()))
                session.commit()

        logging.warning(
            f"videos - {i+1}/{N_SPLITS_VIDEOS} done - {len(sub_videos_df)} rows"
        )


def _reboot(engine=engine):
    """Reboot database"""

    logging.warning("Rebooting database")
    _drop_all(engine=engine)
    _create_all(engine=engine)
    _boot(engine=engine)


def _export(engine=engine, path="./data/tables/"):
    """ """

    logging.warning("Exporting database")

    pair_dict = [
        ("categ_1.csv", Categ1),
        ("categ_2.csv", Categ2),
        ("channels.csv", Channel),
        ("languages.csv", Language),
        ("status.csv", Status),
        ("users.csv", User),
        ("userschannels.csv", UserChannel),
        ("videos.csv", Video),
    ]

    for fn, Obj in pair_dict:
        logging.warning(f"{fn}")

        with Session(engine) as session:
            results = session.query(Obj).all()

        # logging.warning(results[0])
        results = [i.__dict__ for i in results]
        # logging.warning(results[0])
        results_df = pd.DataFrame(results)
        # logging.warning(results_df.head(1).to_dict())
        cols = [i for i in results_df.columns if i in Obj.__table__.columns.keys()]
        results_df = results_df.loc[:, cols]
        results_df = results_df.drop_duplicates()
        results_df = results_df.loc[:, Obj.__table__.columns.keys()]
        results_df.to_csv(os.path.join(path, fn), index=False)


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
    export = _export
