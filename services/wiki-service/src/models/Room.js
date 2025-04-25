const mongoose = require('mongoose');

const RoomSchema = new mongoose.Schema({
  room_id: {
    type: Number,
    required: true,
    unique: true
  },
  room_name: {
    type: String,
    required: true
  },
  dungeon_id: {
    type: Number,
    required: true
  },
  dungeon_name: {
    type: String,
    required: true
  },
  dungeon_lore: String,
  in_waypoint: String,
  out_waypoint: String,
  rooms_connected: [{
    room_id: Number,
    room_name: String
  }],
  hints: [{
    creation_date: String,
    text: String,
    category: {
      type: String,
      enum: ['Lore', 'Hint', 'Suggestion', 'Bug']
    },
    publish_by: {
      email: String,
      user_name: String,
      creation_date: String,
      country: String
    }
  }],
  monsters: [{
    id: Number,
    name: String,
    place: String,
    type: String,
    man_page: String,
    level: Number,
    exp: Number
  }],
  loot: [{
    id: Number,
    name: String,
    type1: String,
    type2: String,
    weight: String,
    gold: Number
  }]
});

module.exports = mongoose.model('Room', RoomSchema);
