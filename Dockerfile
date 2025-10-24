FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    wget curl unzip gnupg \
    google-chrome-stable \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

ENV CHROME_BIN="/usr/bin/google-chrome"
ENV CHROMEDRIVER_PATH="/usr/bin/chromedriver"

WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
