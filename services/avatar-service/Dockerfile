FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p assets/avatars && chmod 755 assets/avatars

RUN useradd -m appuser
USER appuser

COPY --chown=appuser:appuser . .

EXPOSE 8080

ENV LOAD_AVATARS_ON_STARTUP=false
ENV AVATARS_DIR=/app/assets/avatars
ENV METADATA_FILE=

CMD ["python", "-m", "app.start"]