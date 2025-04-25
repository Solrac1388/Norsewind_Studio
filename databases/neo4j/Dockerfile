FROM neo4j:4.4

# Crear el script de inicialización directamente en el Dockerfile
RUN echo '#!/bin/bash \n\
set -e \n\
\n\
if [ -f "/var/lib/neo4j/neo4j.dump" ]; then \n\
    echo "Restaurando dump de Neo4j..." \n\
    neo4j-admin load --from=/var/lib/neo4j/neo4j.dump --database=neo4j --force \n\
    echo "Dump restaurado exitosamente" \n\
fi \n\
\n\
exec /docker-entrypoint.sh neo4j \n\
' > /init-neo4j.sh && chmod +x /init-neo4j.sh

ENTRYPOINT ["/init-neo4j.sh"]