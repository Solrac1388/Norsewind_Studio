FROM python:3.9-slim

WORKDIR /app

# Instalar dependencias
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Instalar cqlsh
RUN pip install --no-cache-dir cqlsh

# Copiar archivos del proyecto ANTES de crear el script
COPY . .
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Crear script de inicio
RUN echo '#!/bin/bash' > start.sh && \
    echo 'echo "Esperando a que Cassandra esté disponible..."' >> start.sh && \
    echo 'max_retries=30' >> start.sh && \
    echo 'counter=0' >> start.sh && \
    echo 'while ! cqlsh ${CASSANDRA_CONTACT_POINTS:-cassandra} -e "describe keyspaces" > /dev/null 2>&1; do' >> start.sh && \
    echo '    counter=$((counter+1))' >> start.sh && \
    echo '    if [ $counter -ge $max_retries ]; then' >> start.sh && \
    echo '        echo "Error: No se pudo conectar a Cassandra después de $max_retries intentos."' >> start.sh && \
    echo '        exit 1' >> start.sh && \
    echo '    fi' >> start.sh && \
    echo '    echo "Cassandra no disponible, intentando de nuevo en 5 segundos... ($counter/$max_retries)"' >> start.sh && \
    echo '    sleep 5' >> start.sh && \
    echo 'done' >> start.sh && \
    echo 'echo "Cassandra está disponible, iniciando servicio"' >> start.sh && \
    echo 'exec uvicorn app.main:app --host 0.0.0.0 --port 8080' >> start.sh && \
    chmod +x start.sh

# Cambiar a usuario no privilegiado
RUN useradd -m appuser
USER appuser

EXPOSE 8080

CMD ["./start.sh"]