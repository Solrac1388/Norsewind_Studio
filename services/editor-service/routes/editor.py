from flask import Blueprint, jsonify, request
from services.neo4j_service import Neo4jService

editor_bp = Blueprint('editor', __name__, url_prefix='/api/editor')

@editor_bp.route('/loots/<int:loot_id>/rooms', methods=['GET'])
def find_rooms_with_loot(loot_id):
    """
    1. Buscar todas las salas que contengan un tesoro en particular.
    """
    result = Neo4jService.find_rooms_with_loot(loot_id)
    return jsonify(result)

@editor_bp.route('/rooms/<int:room_id>/monsters', methods=['GET'])
def get_monsters_in_room(room_id):
    """
    2. Obtener todos los monstruos que hay en una sala en particular.
    """
    result = Neo4jService.get_monsters_in_room(room_id)
    return jsonify(result)

@editor_bp.route('/monsters/unused', methods=['GET'])
def get_unused_monsters():
    """
    3. Obtener todos los monstruos que no están presentes en ninguna sala.
    """
    result = Neo4jService.get_unused_monsters()
    return jsonify(result)

@editor_bp.route('/paths/shortest', methods=['GET'])
def get_shortest_path():
    """
    4. Calcular el camino más corto de un área a otra área.
    """
    from_area = request.args.get('from')
    to_area = request.args.get('to')
    if not from_area or not to_area:
        return jsonify({'error': 'Both "from" and "to" areas must be provided'}), 400
    result = Neo4jService.get_shortest_path(from_area, to_area)
    return jsonify(result)

@editor_bp.route('/paths/enemies', methods=['GET'])
def get_enemies_in_path():
    """
    5. Mostrar los enemigos que es necesario derrotar para ir de un área a otra.
    """
    from_area = request.args.get('from')
    to_area = request.args.get('to')
    if not from_area or not to_area:
        return jsonify({'error': 'Both "from" and "to" areas must be provided'}), 400
    result = Neo4jService.get_enemies_in_path(from_area, to_area)
    return jsonify(result)

@editor_bp.route('/paths/areas', methods=['GET'])
def get_areas_in_path():
    """
    6. Mostrar las áreas que tengo que recorrer para ir de un área a otra.
    """
    from_area = request.args.get('from')
    to_area = request.args.get('to')
    if not from_area or not to_area:
        return jsonify({'error': 'Both "from" and "to" areas must be provided'}), 400
    result = Neo4jService.get_areas_in_path(from_area, to_area)
    return jsonify(result)

@editor_bp.route('/areas/connections', methods=['POST'])
def create_area_connections():
    """
    7. Crear una nueva arista que conecta las distintas áreas del juego.
    """
    result = Neo4jService.create_area_connections()
    return jsonify(result)

@editor_bp.route('/worldmap', methods=['GET'])
def get_world_map():
    """
    8. Mostrar el mapamundi del juego.
    """
    result = Neo4jService.get_world_map()
    return jsonify(result)

@editor_bp.route('/dungeons/<string:dungeon_name>/gold', methods=['GET'])
def get_dungeon_gold(dungeon_name):
    """
    9. Calcular el total de oro que valen los tesoros de una mazmorra.
    """
    result = Neo4jService.get_dungeon_gold(dungeon_name)
    return jsonify(result)

@editor_bp.route('/dungeons/<string:dungeon_name>/high-level-monsters', methods=['GET'])
def get_high_level_monsters(dungeon_name):
    """
    10. Buscar las salas que contienen los monstruos de más nivel de la mazmorra.
    """
    result = Neo4jService.get_high_level_monsters(dungeon_name)
    return jsonify(result)

@editor_bp.route('/dungeons/<string:dungeon_name>/encounters', methods=['GET'])
def get_encounters_by_exp(dungeon_name):
    """
    11. Calcular la experiencia total de cada uno de los encuentros.
    """
    result = Neo4jService.get_encounters_by_exp(dungeon_name)
    return jsonify(result)