const Room = require('../models/Room');
const User = require('../models/User');

// GET /room
exports.getAllRooms = async (req, res) => {
  try {
    const rooms = await Room.find({}).select('room_id room_name dungeon_id dungeon_name');
    res.json(rooms);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// GET /room/{room_id}
exports.getRoomById = async (req, res) => {
  try {
    const room = await Room.findOne({ room_id: parseInt(req.params.room_id) });
    
    if (!room) {
      return res.status(404).json({ message: 'Habitación no encontrada' });
    }
    
    // Formateamos la respuesta según los requisitos
    const response = {
      idR: room.room_id,
      name: room.room_name,
      inWP: room.in_waypoint,
      outWP: room.out_waypoint,
      monsters: room.monsters,
      loot: room.loot,
      hints: room.hints
    };
    
    res.json(response);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// POST /comment
exports.addComment = async (req, res) => {
  try {
    const { user_email, room_id, text, category } = req.body;
    
    // Validamos categoría
    const validCategories = ['Lore', 'Hint', 'Suggestion', 'Bug'];
    if (!validCategories.includes(category)) {
      return res.status(400).json({ message: 'Categoría no válida' });
    }
    
    // Buscamos el usuario
    const user = await User.findOne({ email: user_email });
    if (!user) {
      return res.status(404).json({ message: 'Usuario no encontrado' });
    }
    
    // Buscamos la habitación
    const room = await Room.findOne({ room_id: parseInt(room_id) });
    if (!room) {
      return res.status(404).json({ message: 'Habitación no encontrada' });
    }
    
    // Creamos el nuevo comentario
    const newHint = {
      creation_date: new Date().toISOString().split('T')[0],
      text,
      category,
      publish_by: {
        email: user.email,
        user_name: user.user_name,
        creation_date: user.creation_date,
        country: user.country
      }
    };
    
    // Añadimos el comentario a la habitación
    room.hints.push(newHint);
    await room.save();
    
    // Añadimos el comentario al usuario
    user.hints.push({
      creation_date: newHint.creation_date,
      text,
      category,
      references_room: {
        room_id: room.room_id,
        room_name: room.room_name,
        dungeon_id: room.dungeon_id,
        dungeon_name: room.dungeon_name
      }
    });
    await user.save();
    
    res.status(201).json(newHint);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};
