# The builder image, used to build the virtual environment
FROM python:3.10-buster as builder

RUN pip install poetry==1.4.2

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock ./
COPY miscellaneous ./miscellaneous

RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR

##############################
FROM python:3.10-slim-buster as runtime

ENV PYTHONUNBUFFERED 1
ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

WORKDIR /app

COPY youtube_analyzer ./youtube_analyzer

ENTRYPOINT ["python", "-m", "youtube_analyzer"]