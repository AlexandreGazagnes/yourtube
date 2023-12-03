FROM python:3.10-buster

RUN pip install poetry==1.7.0

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /code

COPY pyproject.toml poetry.lock ./
RUN touch README.md

RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR

COPY src ./src
COPY .env ./
COPY main.py .env ./

RUN pwd
RUN ls -alh


ENV MODE="main"

# au cas ou
RUN poetry install --without dev 


CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]