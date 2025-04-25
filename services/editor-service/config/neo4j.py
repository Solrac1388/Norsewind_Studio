import os
import time
from neo4j import GraphDatabase

class Neo4jConfig:
    URI = os.environ.get("NEO4J_URI", "bolt://neo4j:7687")
    USER = os.environ.get("NEO4J_USER", "neo4j")
    PASSWORD = os.environ.get("NEO4J_PASSWORD", "password")

def get_neo4j_driver():
    for attempt in range(5):
        try:
            driver = GraphDatabase.driver(
                Neo4jConfig.URI,
                auth=(Neo4jConfig.USER, Neo4jConfig.PASSWORD)
            )
            # Verificación activa de conexión
            with driver.session() as session:
                session.run("RETURN 1")
            return driver
        except Exception as e:
            print(f"Intento {attempt+1}: Error conectando a Neo4j: {str(e)}")
            if attempt < 4:
                time.sleep(5)
    raise ConnectionError("No se pudo conectar a Neo4j después de 5 intentos")