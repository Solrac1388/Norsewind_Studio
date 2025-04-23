FROM python:3.9-slim

WORKDIR /app

# Instalar curl para healthchecks
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Crear usuario no privilegiado
RUN useradd -m appuser
USER appuser

COPY --chown=appuser:appuser . .

EXPOSE 8080

# Script de inicio integrado
CMD echo "Esperando a que Cassandra esté disponible..." && \
    until python -c "from cassandra.cluster import Cluster; Cluster(['$CASSANDRA_CONTACT_POINTS']).connect()" 2>/dev/null; do \
      echo "Cassandra no disponible, reintentando en 5 segundos..." && \
      sleep 5; \
    done && \
    echo "Cassandra está disponible, iniciando servicio..." && \
    uvicorn app.main:app --host 0.0.0.0 --port 8080