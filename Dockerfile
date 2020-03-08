FROM python:3.8-slim
LABEL maintainer="hi@jozo.io"

# Set environment varibles
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install -y build-essential libpq-dev \
    && pip install --upgrade pip \
    && pip install poetry

COPY ["pyproject.toml", "poetry.lock", "/"]
RUN poetry config virtualenvs.create false && poetry install
# TODO install dev packages only during development, not in production
# TODO consider using virtualenv

COPY . /code/
WORKDIR /code/

RUN useradd wagtail \
    && mkdir /home/wagtail \
    && chown -R wagtail /code /home/wagtail
USER wagtail

EXPOSE 8000
HEALTHCHECK --interval=1m --timeout=5s \
    CMD python -c "import requests; requests.get('http://localhost:8000', timeout=5).ok" || exit 1
