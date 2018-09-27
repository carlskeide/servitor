FROM python:3.6-alpine

RUN apk add --no-cache gcc python3-dev musl-dev linux-headers

RUN adduser -S app
RUN mkdir -p /app /conf

EXPOSE 3031 5000
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /app
ENV FLASK_APP servitor

COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

COPY . /app

USER app
WORKDIR /app

CMD ["flask", "run", "-h", "0.0.0.0"]
