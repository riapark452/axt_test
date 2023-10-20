FROM python:3.10.9-slim-buster

RUN apt-get update && \
    apt-get install -y gcc libpq-dev && \
    apt clean && \
    rm -rf /var/cache/apt/*

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=utf-8

COPY . /src

RUN pip install -U pip && \
    pip install --no-cache-dir -r src/requirements.txt

WORKDIR /src

CMD ["./scripts/start-dev.sh"]