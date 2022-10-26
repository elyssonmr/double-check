FROM python:3.10-alpine

WORKDIR /app
COPY . .
RUN apk add --no-cache --virtual .build-deps gcc musl-dev libffi-dev linux-headers build-base \
    && pip install -U setuptools pip \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del .build-deps
