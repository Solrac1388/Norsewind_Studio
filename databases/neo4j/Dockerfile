FROM neo4j:5.13.0

# Instalar plugin APOC
ENV NEO4J_PLUGINS='["apoc"]'
ENV NEO4J_dbms_security_procedures_unrestricted="apoc.*"

# Copiar script de inicialización Cypher
COPY databases/neo4j/scripts/init-data.cypher /var/lib/neo4j/import/init-data.cypher

# Iniciar Neo4j directamente sin script intermedio
ENTRYPOINT ["sh", "-c", "\
if [ -f \"/backups/neo4j.dump\" ]; then \
  neo4j-admin database load neo4j --from-path=/backups --overwrite-destination; \
fi && \
exec neo4j console --verbose"]