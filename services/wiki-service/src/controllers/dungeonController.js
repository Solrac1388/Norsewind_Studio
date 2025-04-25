const Room = require('../models/Room');

// GET /dungeon
exports.getAllDungeons = async (req, res) => {
  try {
    // Obtenemos las habitaciones y agrupamos por dungeon_id
    const rooms = await Room.find({}).select('dungeon_id dungeon_name dungeon_lore');
    
    // Crear un mapa para agrupar por dungeon_id
    const dungeonMap = new Map();
    
    rooms.forEach(room => {
      if (!dungeonMap.has(room.dungeon_id)) {
        dungeonMap.set(room.dungeon_id, {
          id: room.dungeon_id,
          name: room.dungeon_name,
          lore: room.dungeon_lore
        });
      }
    });
    
    // Convertir el mapa a un array
    const dungeons = Array.from(dungeonMap.values());
    
    res.json(dungeons);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// GET /dungeon/{dungeon_id}
exports.getDungeonById = async (req, res) => {
  try {
    const dungeonId = parseInt(req.params.dungeon_id);
    
    // Obtenemos todas las habitaciones de la mazmorra
    const rooms = await Room.find({ dungeon_id: dungeonId });
    
    if (rooms.length === 0) {
      return res.status(404).json({ message: 'Mazmorra no encontrada' });
    }
    
    // Extraemos información básica de la mazmorra
    const dungeonInfo = {
      id: dungeonId,
      name: rooms[0].dungeon_name,
      lore: rooms[0].dungeon_lore,
      rooms: []
    };
    
    // Procesamos cada habitación para extraer la información requerida
    rooms.forEach(room => {
      // Contamos los comentarios por categoría
      const hintCounts = {};
      room.hints.forEach(hint => {
        hintCounts[hint.category] = (hintCounts[hint.category] || 0) + 1;
      });
      
      // Añadimos información de la habitación al resultado
      dungeonInfo.rooms.push({
        id: room.room_id,
        name: room.room_name,
        connections: room.rooms_connected,
        monsters: room.monsters.map(m => ({ id: m.id, name: m.name })),
        loot: room.loot.map(l => ({ id: l.id, name: l.name })),
        hint_counts: hintCounts
      });
    });
    
    res.json(dungeonInfo);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};
