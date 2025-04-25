from config.neo4j import get_neo4j_driver

class Neo4jService:
    @staticmethod
    def query(cypher, params=None):
        """
        Execute a Cypher query and return the results.
        """
        driver = get_neo4j_driver()
        try:
            with driver.session() as session:
                result = session.run(cypher, params)
                return [record.data() for record in result]
        finally:
            driver.close()

    @staticmethod
    def find_rooms_with_loot(loot_id):
        """
        1. Buscar todas las salas que contengan un tesoro en particular.
        """
        query = """
        MATCH (l:Loot {id: $loot_id})<-[:CONTAINS]-(r:Room)
        RETURN r.room_id AS id, r.room_name AS name, r.dungeon_name AS dungeon
        """
        return Neo4jService.query(query, {"loot_id": loot_id})

    @staticmethod
    def get_monsters_in_room(room_id):
        """
        2. Obtener todos los monstruos que hay en una sala en particular.
        """
        query = """
        MATCH (r:Room {room_id: $room_id})-[:CONTAINS]->(m:Monster)
        RETURN m.id AS id, m.name AS name, m.level AS level, m.type AS type
        """
        return Neo4jService.query(query, {"room_id": room_id})

    @staticmethod
    def get_unused_monsters():
        """
        3. Obtener todos los monstruos que no están presentes en ninguna sala.
        """
        query = """
        MATCH (m:Monster)
        WHERE NOT (m)<-[:CONTAINS]-()
        RETURN m.id AS id, m.name AS name, m.level AS level
        """
        return Neo4jService.query(query)

    @staticmethod
    def get_shortest_path(from_area, to_area):
        """
        4. Calcular el camino más corto de un área a otra área.
        """
        query = """
        MATCH path = shortestPath((a1:Area {name: $from_area})-[:IS_CONNECTED*]-(a2:Area {name: $to_area}))
        RETURN [node in nodes(path) | node.name] AS areas, length(path) AS path_length
        """
        return Neo4jService.query(query, {"from_area": from_area, "to_area": to_area})

    @staticmethod
    def get_enemies_in_path(from_area, to_area):
        """
        5. Mostrar los enemigos que es necesario derrotar para ir de un área a otra.
        """
        query = """
        MATCH path = shortestPath((a1:Area {name: $from_area})-[:IS_CONNECTED*]-(a2:Area {name: $to_area}))
        UNWIND nodes(path) AS area_node
        MATCH (area_node)<-[:IS_CONNECTED]-(r:Room)-[:CONTAINS]->(m:Monster)
        RETURN DISTINCT m.id AS id, m.name AS name, m.level AS level, r.room_id AS room_id
        """
        return Neo4jService.query(query, {"from_area": from_area, "to_area": to_area})

    @staticmethod
    def get_areas_in_path(from_area, to_area):
        """
        6. Mostrar las áreas que tengo que recorrer para ir de un área a otra.
        """
        query = """
        MATCH path = shortestPath((a1:Area {name: $from_area})-[:IS_CONNECTED*]-(a2:Area {name: $to_area}))
        RETURN [node in nodes(path) | node.name] AS areas
        """
        return Neo4jService.query(query, {"from_area": from_area, "to_area": to_area})

    @staticmethod
    def create_area_connections():
        """
        7. Crear una nueva arista que conecta las distintas áreas del juego.
        """
        query = """
        MATCH (a1:Area)<-[:IS_CONNECTED]-(r1:Room),
              (a2:Area)<-[:IS_CONNECTED]-(r2:Room)
        WHERE a1 <> a2 AND r1.dungeon_name = r2.dungeon_name
        WITH a1, a2, r1.dungeon_name AS dungeon,
             shortestPath((a1)-[:IS_CONNECTED*]-(a2)) AS path
        MERGE (a1)-[c:CONNECTED_BY {dungeon: dungeon, weight: length(path)}]->(a2)
        RETURN a1.name AS area1, a2.name AS area2, c.dungeon AS dungeon, c.weight AS weight
        """
        return Neo4jService.query(query)

    @staticmethod
    def get_world_map():
        """
        8. Mostrar el mapamundi del juego.
        """
        query = """
        MATCH (a:Area)
        OPTIONAL MATCH (a)-[r:IS_CONNECTED]-(a2:Area)
        RETURN a.name AS area, collect(a2.name) AS connected_areas
        """
        return Neo4jService.query(query)

    @staticmethod
    def get_dungeon_gold(dungeon_name):
        """
        9. Calcular el total de oro que valen los tesoros de una mazmorra.
        """
        query = """
        MATCH (r:Room)-[:CONTAINS]->(l:Loot)
        WHERE r.dungeon_name = $dungeon_name
        RETURN sum(l.gold) AS total_gold
        """
        return Neo4jService.query(query, {"dungeon_name": dungeon_name})

    @staticmethod
    def get_high_level_monsters(dungeon_name):
        """
        10. Buscar las salas que contienen los monstruos de más nivel de la mazmorra.
        """
        query = """
        MATCH (r:Room)-[:CONTAINS]->(m:Monster)
        WHERE r.dungeon_name = $dungeon_name
        WITH max(m.level) AS max_level
        MATCH (r:Room)-[:CONTAINS]->(m:Monster)
        WHERE r.dungeon_name = $dungeon_name AND m.level = max_level
        RETURN r.room_id AS room_id, r.room_name AS room_name, m.id AS monster_id, m.name AS monster_name, m.level AS level
        """
        return Neo4jService.query(query, {"dungeon_name": dungeon_name})

    @staticmethod
    def get_encounters_by_exp(dungeon_name):
        """
        11. Calcular la experiencia total de cada uno de los encuentros.
        """
        query = """
        MATCH (r:Room)-[:CONTAINS]->(m:Monster)
        WHERE r.dungeon_name = $dungeon_name
        WITH r, sum(m.exp) AS total_exp
        RETURN r.room_id AS room_id, r.room_name AS room_name, total_exp
        ORDER BY total_exp DESC
        """
        return Neo4jService.query(query, {"dungeon_name": dungeon_name})