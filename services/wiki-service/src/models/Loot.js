const mongoose = require('mongoose');

const LootSchema = new mongoose.Schema({
  id: {
    type: Number,
    required: true,
    unique: true
  },
  name: {
    type: String,
    required: true
  },
  type1: String,
  type2: String,
  weight: String,
  gold: Number
});

module.exports = mongoose.model('Loot', LootSchema);
