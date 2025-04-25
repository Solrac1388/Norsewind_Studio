const mongoose = require('mongoose');

const MonsterSchema = new mongoose.Schema({
  id: {
    type: Number,
    required: true,
    unique: true
  },
  name: {
    type: String,
    required: true
  },
  place: String,
  type: String,
  man_page: String,
  level: Number,
  exp: Number
});

module.exports = mongoose.model('Monster', MonsterSchema);
