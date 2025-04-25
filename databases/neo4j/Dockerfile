FROM neo4j:5.13.0

# Instalar plugin APOC
ENV NEO4J_PLUGINS='["apoc"]'
ENV NEO4J_dbms_security_procedures_unrestricted="apoc.*"

# Copiar script de inicialización Cypher
COPY databases/neo4j/scripts/init-data.cypher /var/lib/neo4j/import/init-data.cypher

# Iniciar Neo4j directamente sin script intermedio
ENTRYPOINT ["sh", "-c", "\
if [ -f \"/backups/neo4j.dump\" ]; then \
    echo \"Restaurando dump de Neo4j...\" && \
    neo4j-admin database load neo4j --from-path=/backups --overwrite-destination=true && \
    echo \"Dump restaurado exitosamente\"; \
else \
    echo \"Inicializando base de datos con datos de ejemplo...\"; \
    # Iniciar proceso de Neo4j en segundo plano para ejecutar comandos\
    neo4j start && \
    sleep 20 && \
    cypher-shell -u neo4j -p password --file /var/lib/neo4j/import/init-data.cypher && \
    echo \"Base de datos inicializada\" && \
    neo4j stop && \
    sleep 5; \
fi && \
# Ejecutar Neo4j normalmente\
exec neo4j console\
"]