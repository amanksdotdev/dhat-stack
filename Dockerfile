ARG PYTHON_VERSION=3.12-slim

FROM python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /code

WORKDIR /code

RUN pip install uv
COPY pyproject.toml uv.lock /code/
RUN uv venv
RUN uv sync 
COPY . /code
RUN apt-get update && apt-get install -y \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*
RUN uv run manage.py collectstatic --noinput
RUN chmod +x startup.sh

EXPOSE 8000
ENTRYPOINT ["./startup.sh"]
