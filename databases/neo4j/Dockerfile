FROM neo4j:5.13.0

# Instalar plugin APOC
ENV NEO4J_PLUGINS='["apoc"]'

# Crear el script de inicialización con la ruta correcta
RUN echo '#!/bin/bash \n\
set -e \n\
\n\
if [ -f "/backups/neo4j.dump" ]; then \n\
    echo "Restaurando dump de Neo4j..." \n\
    neo4j-admin database load neo4j --from-path=/backups --overwrite-destination=true \n\
    echo "Dump restaurado exitosamente" \n\
fi \n\
\n\
# Ejecutar el comando directamente en lugar de llamar a un script\n\
exec /startup/docker-entrypoint.sh neo4j \n\
' > /init-neo4j.sh && chmod +x /init-neo4j.sh

ENTRYPOINT ["/init-neo4j.sh"]