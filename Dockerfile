FROM python:3.10-slim AS compile-image
LABEL maintainer="hi@jozo.io"

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    libffi-dev \
    libpq-dev \
    && python -m venv "/opt/venv" \
    && . "/opt/venv/bin/activate" \
    && pip install --upgrade pip \
    && pip install poetry

COPY ["src/pyproject.toml", "src/poetry.lock", "/root/"]
RUN cd "/root/" && . "/opt/venv/bin/activate" && poetry install


FROM python:3.10-slim AS runtime-image
COPY --from=compile-image  /opt/venv /opt/venv

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
      libcairo2 \
      libpq5 \
      gettext \
    && apt-get clean

ENV PYTHONUNBUFFERED=1
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
EXPOSE 8000

RUN useradd -m wagtail && chown -R wagtail:wagtail $VIRTUAL_ENV
USER wagtail

COPY --chown=wagtail:wagtail ./src /code
WORKDIR /code/
