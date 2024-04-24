const User = require('../models/User');

module.exports = {
    async createUser(userData) {
        try {
            return await User.create(userData);
        } catch (error) {
            throw new Error(error.message);
        }
    },
    async findByUsername(username) {
        try {
            return await User.findOne({ username });
        } catch (error) {
            throw new Error(error.message);
        }
    }
};
