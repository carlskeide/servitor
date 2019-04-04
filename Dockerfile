FROM python:3.6-alpine

ENV PYTHONUNBUFFERED 1
EXPOSE 3031 8000

RUN adduser -D app &&\
    mkdir -p /app

RUN apk add --no-cache gcc g++ python3-dev musl-dev linux-headers

COPY requirements.txt /app/
RUN pip install --no-cache-dir \
    -r /app/requirements.txt

COPY . /app

WORKDIR /app
USER app
CMD ["uwsgi", "uwsgi.ini"]
