const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const connectDB = require('./config/db');
require('dotenv').config();

// Rutas
const dungeonRoutes = require('./routes/dungeonRoutes');
const lootRoutes = require('./routes/lootRoutes');
const monsterRoutes = require('./routes/monsterRoutes');
const roomRoutes = require('./routes/roomRoutes');
const userRoutes = require('./routes/userRoutes');

// Conexión a la base de datos
connectDB();

const app = express();

// Middleware
app.use(helmet());
app.use(cors());
app.use(express.json());

// Definición de rutas
app.use('/dungeon', dungeonRoutes);
app.use('/loot', lootRoutes);
app.use('/monster', monsterRoutes);
app.use('/room', roomRoutes);
app.use('/user', userRoutes);

// Ruta raíz
app.get('/', (req, res) => {
  res.send('API de Jotun\'s Lair Wiki');
});

const PORT = process.env.PORT || 8080;

app.listen(PORT, () => {
  console.log(`Servidor ejecutándose en el puerto ${PORT}`);
});
