FROM python:3.8-slim AS compile-image
LABEL maintainer="hi@jozo.io"

RUN apt-get update
RUN apt-get install -y --no-install-recommends build-essential libpq-dev \
    && pip install --upgrade pip \
    && pip install poetry

COPY ["pyproject.toml", "poetry.lock", "/root/"]
RUN cd /root \
    && poetry config virtualenvs.in-project true \
    && poetry install

# TODO install dev packages only during development, not in production


FROM python:3.8-slim AS runtime-image
COPY --from=compile-image /root/.venv /opt/venv
# ldd /root/.venv/lib/python3.8/site-packages/psycopg2/_psycopg.cpython-38-x86_64-linux-gnu.so
COPY --from=compile-image ["/usr/lib/x86_64-linux-gnu/libpq.so.5", "/lib/x86_64-linux-gnu/libpthread.so.0", "/lib/x86_64-linux-gnu/libc.so.6", "/usr/lib/x86_64-linux-gnu/libgssapi_krb5.so.2", "/usr/lib/x86_64-linux-gnu/libldap_r-2.4.so.2", "/lib/x86_64-linux-gnu/libdl.so.2", "/usr/lib/x86_64-linux-gnu/libkrb5.so.3", "/usr/lib/x86_64-linux-gnu/libk5crypto.so.3", "/lib/x86_64-linux-gnu/libcom_err.so.2", "/usr/lib/x86_64-linux-gnu/libkrb5support.so.0", "/lib/x86_64-linux-gnu/libkeyutils.so.1", "/lib/x86_64-linux-gnu/libresolv.so.2", "/usr/lib/x86_64-linux-gnu/liblber-2.4.so.2", "/usr/lib/x86_64-linux-gnu/libsasl2.so.2", "/usr/lib/"]

ENV PYTHONUNBUFFERED=1
ENV PATH="/opt/venv/bin:$PATH"
EXPOSE 8000

RUN useradd -m wagtail
USER wagtail

COPY --chown=wagtail:wagtail . /code/
WORKDIR /code/
