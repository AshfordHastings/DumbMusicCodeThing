FROM python:3.9-slim

# RUN apt-get update && apt-get install -y \
#     libpq-dev

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "--config", "gunicorn_config.py", "gunicorn_config:app"]