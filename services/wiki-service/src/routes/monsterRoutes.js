const express = require('express');
const router = express.Router();
const monsterController = require('../controllers/monsterController');

// GET /monster
router.get('/', monsterController.getAllMonsters);

// GET /monster/{monster_id}
router.get('/:monster_id', monsterController.getMonsterById);

// DELETE /monster/{monster_id}
router.delete('/:monster_id', monsterController.deleteMonster);

module.exports = router;
