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


url_object = URL.create(
    drivername="mysql+mysqlconnector",
    username="root",
    password="password",  # plain (unescaped) text
    host="localhost",
    database="yourdb",
)


engine = create_engine(url_object)
session = Session(engine)


from src.models.base import Base
from src.models.categ_1 import Categ1
from src.models.categ_2 import Categ2
from src.models.channels import Channels
from src.models.languages import Language
from src.models.videos import Videos


# class Db:
#     categ_1 = Categ1
#     categ_2 = Categ2
#     channels = Channels
#     languages = Language
#     language = Language
#     videos = Videos
#     engine = engine
#     session = session
