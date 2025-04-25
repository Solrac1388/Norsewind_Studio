FROM neo4j:5.13.0

# Instalar plugin APOC
ENV NEO4J_PLUGINS='["apoc"]'
ENV NEO4J_dbms_security_procedures_unrestricted="apoc.*"

# Copiar scripts
COPY databases/neo4j/scripts/init-data.cypher /scripts/

# Crear script de inicialización
RUN echo '#!/bin/bash \n\
set -e \n\
\n\
if [ -f "/backups/neo4j.dump" ]; then \n\
    echo "Restaurando dump de Neo4j..." \n\
    neo4j-admin database load neo4j --from-path=/backups --overwrite-destination=true \n\
    echo "Dump restaurado exitosamente" \n\
else \n\
    echo "Inicializando con datos de ejemplo..." \n\
    mkdir -p /scripts \n\
    /var/lib/neo4j/bin/neo4j start & \n\
    echo "Esperando a Neo4j..." \n\
    sleep 30 \n\
    cat /scripts/init-data.cypher | cypher-shell -u neo4j -p password \n\
    echo "Base de datos inicializada" \n\
    /var/lib/neo4j/bin/neo4j stop \n\
    sleep 5 \n\
fi \n\
\n\
exec /docker-entrypoint.sh neo4j \n\
' > /init-neo4j.sh && chmod +x /init-neo4j.sh

ENTRYPOINT ["/init-neo4j.sh"]