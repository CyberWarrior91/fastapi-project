FROM python:3.10

RUN pip install poetry==1.5.1

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

RUN mkdir /fastapi_app

WORKDIR /fastapi_app

COPY pyproject.toml poetry.lock ./
RUN touch README.md

RUN poetry install --no-root && rm -rf $POETRY_CACHE_DIR

COPY . .

RUN chmod a+x docker/*.sh

RUN poetry run alembic upgrade head

CMD poetry run gunicorn src.main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
