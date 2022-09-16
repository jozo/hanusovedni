FROM python:3.10.5-slim AS compile-image
LABEL maintainer="hi@jozo.io"

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    libffi-dev \
    libpq-dev \
    && python -m venv "/opt/venv" \
    && . "/opt/venv/bin/activate" \
    && pip install --upgrade pip

COPY ["src/requirements/development.txt", "/root/"]
RUN cd "/root/" && . "/opt/venv/bin/activate" && pip install -r development.txt


FROM python:3.10.5-slim AS runtime-image
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

RUN useradd -m wagtail && chown -R wagtail:wagtail $VIRTUAL_ENV
USER wagtail

COPY --chown=wagtail:wagtail ./src /code
WORKDIR /code/
