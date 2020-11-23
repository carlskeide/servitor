FROM python:3.8-alpine

RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    libressl-dev \
    linux-headers \
    python3-dev

# App settings
ENV PYTHONUNBUFFERED 1
EXPOSE 3031 8080

RUN adduser -D app &&\
    mkdir -p /app

# Setup python env
COPY ./requirements.txt /
RUN pip install --quiet --no-cache-dir --upgrade \
    -r /requirements.txt

# Copy and install source
COPY . /app
RUN pip install --quiet -e /app

# Invocation
WORKDIR /app
USER app
CMD ["uwsgi", "/app/uwsgi.ini"]
