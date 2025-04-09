FROM python:3.9-slim

WORKDIR /app

# Instalar dependencias del sistema necesarias para pillow y torch
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Crear directorio para los avatares con los permisos adecuados
RUN mkdir -p assets/avatars && chmod 755 assets/avatars

# Cambiar a un usuario no privilegiado para mayor seguridad
RUN useradd -m appuser
USER appuser

COPY --chown=appuser:appuser . .

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]