const express = require('express');
const router = express.Router();
const dungeonController = require('../controllers/dungeonController');

// GET /dungeon
router.get('/', dungeonController.getAllDungeons);

// GET /dungeon/{dungeon_id}
router.get('/:dungeon_id', dungeonController.getDungeonById);

module.exports = router;
