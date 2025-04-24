FROM python:3.9-slim

WORKDIR /app

# Instalar dependencias
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Instalar cqlsh para verificar conexión con Cassandra
RUN pip install --no-cache-dir cqlsh

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Crear directorios necesarios
RUN mkdir -p cql

# Crear usuario no privilegiado
RUN useradd -m appuser
USER appuser

COPY --chown=appuser:appuser . .

EXPOSE 8080

# Crear script de inicio con lógica mejorada de espera
RUN echo '#!/bin/bash \n\
echo "Esperando a que Cassandra esté disponible..." \n\
max_retries=30 \n\
counter=0 \n\
while ! cqlsh ${CASSANDRA_CONTACT_POINTS:-cassandra} -e "describe keyspaces" > /dev/null 2>&1; do \n\
    counter=$((counter+1)) \n\
    if [ $counter -ge $max_retries ]; then \n\
        echo "Error: No se pudo conectar a Cassandra después de $max_retries intentos." \n\
        exit 1 \n\
    fi \n\
    echo "Cassandra no disponible, intentando de nuevo en 5 segundos... ($counter/$max_retries)" \n\
    sleep 5 \n\
done \n\
echo "Cassandra está disponible, iniciando servicio" \n\
exec uvicorn app.main:app --host 0.0.0.0 --port 8080 \n\
' > /app/start.sh && chmod +x /app/start.sh

CMD ["/app/start.sh"]