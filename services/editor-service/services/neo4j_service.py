import os
import time
from neo4j import GraphDatabase

class Neo4jConfig:
    URI = os.environ.get("NEO4J_URI", "bolt://neo4j:7687")
    USER = os.environ.get("NEO4J_USER", "neo4j")
    PASSWORD = os.environ.get("NEO4J_PASSWORD", "password")

class Neo4jService:
    _driver = None

    @classmethod
    def get_driver(cls):
        if cls._driver is None:
            for attempt in range(5):
                try:
                    cls._driver = GraphDatabase.driver(
                        Neo4jConfig.URI,
                        auth=(Neo4jConfig.USER, Neo4jConfig.PASSWORD)
                    )
                    # Verificación activa de conexión
                    with cls._driver.session() as session:
                        session.run("RETURN 1")
                    print(f"Conexión a Neo4j establecida correctamente en {Neo4jConfig.URI}")
                    break
                except Exception as e:
                    print(f"Intento {attempt+1}: Error conectando a Neo4j: {str(e)}")
                    if attempt < 4:  # No dormir en el último intento
                        time.sleep(5)
            else:
                raise ConnectionError("No se pudo conectar a Neo4j después de 5 intentos")
        return cls._driver

    @classmethod
    def query(cls, cypher, params=None):
        try:
            driver = cls.get_driver()
            with driver.session() as session:
                result = session.run(cypher, params or {})
                return [record.data() for record in result]
        except Exception as e:
            app.logger.error(f"Error en consulta Neo4j: {str(e)}")
            # Re-lanzar como error HTTP 500 con detalles
            raise Exception(f"Error de base de datos: {str(e)}")

    # Implementación de métodos específicos
    @classmethod
    def find_rooms_with_loot(cls, loot_id):
        query = """
        MATCH (l:Loot {id: $loot_id})<-[:CONTAINS]-(r:Room)
        RETURN r.id AS room_id, r.name AS room_name, r.description AS room_description
        """
        return cls.query(query, {"loot_id": loot_id})

    @classmethod
    def get_monsters_in_room(cls, room_id):
        query = """
        MATCH (r:Room {id: $room_id})-[:HAS]->(m:Monster)
        RETURN m.id AS monster_id, m.name AS monster_name, m.level AS monster_level
        """
        return cls.query(query, {"room_id": room_id})

    @classmethod
    def get_unused_monsters(cls):
        query = """
        MATCH (m:Monster)
        WHERE NOT (m)<-[:HAS]-()
        RETURN m.id AS monster_id, m.name AS monster_name, m.level AS monster_level
        """
        return cls.query(query)

    @classmethod
    def get_shortest_path(cls, from_area, to_area):
        query = """
        MATCH path = shortestPath((a1:Area {name: $from_area})-[:CONNECTS_TO*]-(a2:Area {name: $to_area}))
        RETURN [node in nodes(path) | node.name] AS path
        """
        return cls.query(query, {"from_area": from_area, "to_area": to_area})

    @classmethod
    def get_enemies_in_path(cls, from_area, to_area):
        query = """
        MATCH path = shortestPath((a1:Area {name: $from_area})-[:CONNECTS_TO*]-(a2:Area {name: $to_area}))
        MATCH (a)-[:CONTAINS]->(e:Enemy)
        WHERE a IN nodes(path)
        RETURN a.name AS area_name, collect(e.name) AS enemies
        """
        return cls.query(query, {"from_area": from_area, "to_area": to_area})

    @classmethod
    def get_areas_in_path(cls, from_area, to_area):
        query = """
        MATCH path = shortestPath((a1:Area {name: $from_area})-[:CONNECTS_TO*]-(a2:Area {name: $to_area}))
        RETURN [node in nodes(path) | node.name] AS areas
        """
        return cls.query(query, {"from_area": from_area, "to_area": to_area})

    @classmethod
    def create_area_connections(cls):
        query = """
        MATCH (a1:Area), (a2:Area)
        WHERE a1 <> a2 AND NOT (a1)-[:CONNECTS_TO]-(a2)
        WITH a1, a2 LIMIT 1
        CREATE (a1)-[:CONNECTS_TO]->(a2)
        RETURN a1.name AS from_area, a2.name AS to_area
        """
        return cls.query(query)

    @classmethod
    def get_world_map(cls):
        query = """
        MATCH (a:Area)
        OPTIONAL MATCH (a)-[c:CONNECTS_TO]->(b:Area)
        RETURN a.name AS area, collect(b.name) AS connected_areas
        """
        return cls.query(query)

    @classmethod
    def get_dungeon_gold(cls, dungeon_name):
        query = """
        MATCH (r:Room {dungeon_name: $dungeon_name})-[:CONTAINS]->(l:Loot)
        RETURN sum(l.value) AS total_gold
        """
        result = cls.query(query, {"dungeon_name": dungeon_name})
        return result if result else [{"total_gold": 0}]

    @classmethod
    def get_high_level_monsters(cls, dungeon_name):
        query = """
        MATCH (r:Room {dungeon_name: $dungeon_name})-[:HAS]->(m:Monster)
        WITH max(m.level) AS max_level
        MATCH (r:Room {dungeon_name: $dungeon_name})-[:HAS]->(m:Monster {level: max_level})
        RETURN r.name AS room_name, m.name AS monster_name, m.level AS monster_level
        """
        return cls.query(query, {"dungeon_name": dungeon_name})

    @classmethod
    def get_encounters_by_exp(cls, dungeon_name):
        query = """
        MATCH (r:Room {dungeon_name: $dungeon_name})-[:HAS]->(m:Monster)
        WITH r, sum(m.exp) AS total_exp
        RETURN r.name AS room_name, total_exp
        ORDER BY total_exp DESC
        """
        return cls.query(query, {"dungeon_name": dungeon_name})
