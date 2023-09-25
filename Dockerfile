FROM python:3.9

ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update && apt-get install -y ffmpeg

COPY req.txt /app/
RUN pip install --no-cache-dir -r req.txt

COPY . /app/

CMD ["sh", "-c", "python manage.py migrate & python manage.py runserver 0.0.0.0:8000 & celery -A config worker -l info"]
