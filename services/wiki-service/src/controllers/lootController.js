const Loot = require('../models/Loot');
const Room = require('../models/Room');

// GET /loot
exports.getAllLoot = async (req, res) => {
  try {
    const loot = await Loot.find({});
    res.json(loot);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// GET /loot/{loot_id}
exports.getLootById = async (req, res) => {
  try {
    const loot = await Loot.findOne({ id: parseInt(req.params.loot_id) });
    
    if (!loot) {
      return res.status(404).json({ message: 'Tesoro no encontrado' });
    }
    
    res.json(loot);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// DELETE /loot/{loot_id}
exports.deleteLoot = async (req, res) => {
  try {
    const lootId = parseInt(req.params.loot_id);
    
    // Buscamos y eliminamos el tesoro
    const loot = await Loot.findOneAndDelete({ id: lootId });
    
    if (!loot) {
      return res.status(404).json({ message: 'Tesoro no encontrado' });
    }
    
    // Actualizamos todas las habitaciones que contienen este tesoro
    await Room.updateMany(
      { "loot.id": lootId },
      { $pull: { loot: { id: lootId } } }
    );
    
    res.json({ message: 'Tesoro eliminado correctamente' });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};
