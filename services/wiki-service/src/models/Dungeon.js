const mongoose = require('mongoose');

const DungeonSchema = new mongoose.Schema({
  dungeon_id: {
    type: Number,
    required: true,
    unique: true
  },
  name: {
    type: String,
    required: true
  },
  lore: String
});

module.exports = mongoose.model('Dungeon', DungeonSchema);
