FROM python:3.8-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /code

COPY . .

RUN set -e; \
    pip install --no-cache-dir -r requirements.txt && \
    pip check
