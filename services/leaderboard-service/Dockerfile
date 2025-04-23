FROM python:3.9-slim

WORKDIR /app

# Instalar dependencias
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    python-is-python3 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Instalar cqlsh para verificar conexión con Cassandra
RUN pip install --no-cache-dir cqlsh

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Crear usuario no privilegiado
RUN useradd -m appuser
USER appuser

COPY --chown=appuser:appuser . .

EXPOSE 8080

# Script de inicio integrado con espera para Cassandra
CMD echo "Esperando a que Cassandra esté disponible..." && \
    while ! cqlsh ${CASSANDRA_CONTACT_POINTS:-cassandra} -e "describe keyspaces" >/dev/null 2>&1; do \
      echo "Cassandra no disponible, esperando 5 segundos..." && \
      sleep 5; \
    done && \
    echo "Cassandra está disponible, iniciando servicio" && \
    uvicorn app.main:app --host 0.0.0.0 --port 8080