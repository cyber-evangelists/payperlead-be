FROM python:3.10-buster

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml .

RUN python -m poetry install

COPY . .

CMD python -m poetry run uvicorn lib.main:app --host 0.0.0.0
