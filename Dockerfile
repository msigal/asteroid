FROM python:3.7.2-alpine

ENV PYTHONUNBUFFERED=1
ARG CURRENT_ENV=${CURRENT_ENV}
ENV DOCKERIZE_VERSION=v0.6.1

RUN apk update && apk add postgresql-dev build-base libxml2-dev libxslt-dev libffi-dev && \
    wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz

RUN ln -s /root/.poetry/bin/poetry /usr/bin/poetry && \
    wget https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py && \
    python3 ./get-poetry.py --version 1.0.2 && \
    poetry config virtualenvs.create false && \
    rm ./get-poetry.py

COPY pyproject.toml poetry.lock /opt/app/

WORKDIR /opt/app/
RUN /bin/sh -c 'poetry install $(test "$CURRENT_ENV" == prod && echo "--no-dev") --no-interaction --no-ansi'

COPY . /opt/app

CMD ["gunicorn", "-c", "gunicorn_conf.py", "asteroid.wsgi"]
