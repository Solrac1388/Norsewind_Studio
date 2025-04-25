FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Cambiar a un usuario no privilegiado para mayor seguridad
RUN useradd -m appuser
USER appuser

COPY --chown=appuser:appuser . .

EXPOSE 8080

# Simplificar el comando sin los argumentos problemáticos
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]