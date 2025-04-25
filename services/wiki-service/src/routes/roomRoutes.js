const express = require('express');
const router = express.Router();
const roomController = require('../controllers/roomController');

// GET /room
router.get('/', roomController.getAllRooms);

// GET /room/{room_id}
router.get('/:room_id', roomController.getRoomById);

// POST /comment
router.post('/comment', roomController.addComment);

module.exports = router;
