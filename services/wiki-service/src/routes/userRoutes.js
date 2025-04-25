const express = require('express');
const router = express.Router();
const userController = require('../controllers/userController');

// GET /user
router.get('/', userController.getAllUsers);

// GET /user/{email}
router.get('/:email', userController.getUserByEmail);

module.exports = router;
