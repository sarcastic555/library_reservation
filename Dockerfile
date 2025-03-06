FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    curl gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /src
COPY ./pyproject.toml poetry.lock /src/

ENV POETRY_HOME="/"
ENV PATH="/bin:$PATH"
RUN curl -sSL https://install.python-poetry.org | python3 -
# poetryが仮想環境を作ってしまうと、container内で再度peotry installが必要になる
# https://qiita.com/kakeruuuun/questions/1432b997092988262d0c
RUN poetry config virtualenvs.create false
RUN cat pyproject.toml
RUN poetry install --no-root
