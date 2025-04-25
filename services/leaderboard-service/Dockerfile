FROM python:3.9-slim

WORKDIR /app

# Instalar dependencias básicas
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir cqlsh

# Copiar código de la aplicación
COPY . .

EXPOSE 8080

# Usar script embebido en el CMD
CMD bash -c 'echo "Esperando a que Cassandra esté disponible..." && \
    max_retries=30 && \
    counter=0 && \
    while ! cqlsh ${CASSANDRA_CONTACT_POINTS:-cassandra} -e "describe keyspaces" > /dev/null 2>&1; do \
        counter=$((counter+1)) && \
        if [ $counter -ge $max_retries ]; then \
            echo "Error: No se pudo conectar a Cassandra después de $max_retries intentos." && \
            exit 1; \
        fi && \
        echo "Cassandra no disponible, intentando de nuevo en 5 segundos... ($counter/$max_retries)" && \
        sleep 5; \
    done && \
    echo "Cassandra está disponible, iniciando servicio" && \
    uvicorn app.main:app --host 0.0.0.0 --port 8080'