const mongoose = require('mongoose');

const UserSchema = new mongoose.Schema({
  email: {
    type: String,
    required: true,
    unique: true
  },
  user_name: {
    type: String,
    required: true
  },
  creation_date: {
    type: String,
    required: true
  },
  country: String,
  hints: [{
    creation_date: String,
    text: String,
    category: {
      type: String,
      enum: ['Lore', 'Hint', 'Suggestion', 'Bug']
    },
    references_room: {
      room_id: Number,
      room_name: String,
      dungeon_id: Number,
      dungeon_name: String
    }
  }]
});

module.exports = mongoose.model('User', UserSchema);
