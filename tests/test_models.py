import pytest

from src.models import *


def test_session():
    session


def test_select():
    with Session(engine) as session:
        # query for ``User`` objects

        result = session.query(Language).all()
        # result = session.execute(select(Language)).all()

        print(result)


# q = some_session.query(User, Address)


# def test_create_language():
#     with Session(engine) as session:
#         language = Language(id_language="Es")

#         session.add(language)

#         session.commit()  # write changes to the database
