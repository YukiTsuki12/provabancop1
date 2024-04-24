const express = require('express');
const bodyParser = require('body-parser');
const config = require('./config');
const authRoutes = require('./routes/authRoutes');

const app = express();

app.use(bodyParser.json());

app.use('/auth', authRoutes);

app.listen(config.PORT, () => {
    console.log(`Server is running on port ${config.PORT}`);
});
