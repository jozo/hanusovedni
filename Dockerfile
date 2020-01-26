FROM python:3.8-slim
LABEL maintainer="hi@jozo.io"

# Set environment varibles
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install -y build-essential \
    && pip install --upgrade pip \
    && pip install poetry

COPY ["pyproject.toml", "poetry.lock", "/"]
RUN poetry config virtualenvs.create false && poetry install

COPY . /code/
WORKDIR /code/

RUN useradd wagtail
RUN chown -R wagtail /code
USER wagtail

EXPOSE 8000
