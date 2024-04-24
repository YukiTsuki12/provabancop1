const express = require('express');
const router = express.Router();
const userRepository = require('../repositories/userRepository');

router.post('/register', async (req, res) => {
    try {
        const { username, password } = req.body;
        const existingUser = await userRepository.findByUsername(username);
        if (existingUser) {
            return res.status(400).json({ message: 'Username already exists' });
        }
        const newUser = await userRepository.createUser({ username, password });
        res.status(201).json(newUser);
    } catch (error) {
        res.status(500).json({ message: error.message });
    }
});

module.exports = router;
