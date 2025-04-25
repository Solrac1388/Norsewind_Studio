const Monster = require('../models/Monster');
const Room = require('../models/Room');

// GET /monster
exports.getAllMonsters = async (req, res) => {
  try {
    const monsters = await Monster.find({});
    res.json(monsters);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// GET /monster/{monster_id}
exports.getMonsterById = async (req, res) => {
  try {
    const monster = await Monster.findOne({ id: parseInt(req.params.monster_id) });
    
    if (!monster) {
      return res.status(404).json({ message: 'Monstruo no encontrado' });
    }
    
    res.json(monster);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// DELETE /monster/{monster_id}
exports.deleteMonster = async (req, res) => {
  try {
    const monsterId = parseInt(req.params.monster_id);
    
    // Buscamos y eliminamos el monstruo
    const monster = await Monster.findOneAndDelete({ id: monsterId });
    
    if (!monster) {
      return res.status(404).json({ message: 'Monstruo no encontrado' });
    }
    
    // Actualizamos todas las habitaciones que contienen este monstruo
    await Room.updateMany(
      { "monsters.id": monsterId },
      { $pull: { monsters: { id: monsterId } } }
    );
    
    res.json({ message: 'Monstruo eliminado correctamente' });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};
