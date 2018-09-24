FROM python:3.6-alpine

RUN apk add --no-cache gcc python3-dev musl-dev linux-headers

RUN adduser -S app
RUN mkdir -p /app

EXPOSE 3031 8000
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

COPY . /app

USER app
WORKDIR /app
CMD ["uwsgi",  "/app/uwsgi.ini"]
