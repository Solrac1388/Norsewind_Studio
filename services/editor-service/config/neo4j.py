import os
from neo4j import GraphDatabase

class Neo4jConfig:
    URI = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
    USER = os.environ.get("NEO4J_USER", "neo4j")
    PASSWORD = os.environ.get("NEO4J_PASSWORD", "password")

def get_neo4j_driver():
    driver = GraphDatabase.driver(
        Neo4jConfig.URI,
        auth=(Neo4jConfig.USER, Neo4jConfig.PASSWORD)
    )
    return driver