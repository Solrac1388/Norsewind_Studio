const express = require('express');
const router = express.Router();
const lootController = require('../controllers/lootController');

// GET /loot
router.get('/', lootController.getAllLoot);

// GET /loot/{loot_id}
router.get('/:loot_id', lootController.getLootById);

// DELETE /loot/{loot_id}
router.delete('/:loot_id', lootController.deleteLoot);

module.exports = router;
