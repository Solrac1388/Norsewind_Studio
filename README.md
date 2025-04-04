# Norsewind Studios - The Jötun's Lair

Sistema de backend para el videojuego "The Jötun's Lair", implementado como una arquitectura de microservicios utilizando múltiples bases de datos NoSQL especializadas. Este proyecto demuestra cómo seleccionar e implementar bases de datos específicas según las necesidades de cada componente del sistema.

## 1. Clonar el repositorio

```bash
git clone https://github.com/Solrac1388/Norsewind_Studio.git
cd Norsewind_Studio
```

## 2. Crear directorios para almacenamiento persistente

```bash
mkdir -p databases/neo4j/data
mkdir -p databases/cassandra/data
mkdir -p databases/mongodb/data
mkdir -p databases/redis/data
mkdir -p assets/avatars
```

## 3. Iniciar todos los servicios con Docker Compose

```bash
docker-compose up -d
```

## 4. Verificar que todos los contenedores estén ejecutándose

```bash
docker-compose ps
```

## 5. Instalar el cliente Python

```bash
cd client
pip install -r requirements.txt
```

## 6. Probar la conexión con un ejemplo básico

```bash
python examples/test_connection.py
```

## 7. Para detener todos los servicios

```bash
docker-compose down
```

## 8. Para reiniciar manteniendo los datos

```bash
docker-compose restart
```

---

## Estructura del Proyecto


```
Norsewind_Studio/
│
├── README.md                          # Este documento
├── docker-compose.yml                 # Configuración para desplegar todos los servicios
├── .gitignore                         # Archivos a ignorar por git
│
├── client/                            # Cliente Python para interactuar con todos los servicios
│   ├── jotun_client.py                # Implementación del cliente
│   ├── examples/                      # Ejemplos de uso del cliente
│   └── requirements.txt               # Dependencias del cliente
│
├── services/                          # Todos los microservicios
│   ├── api-gateway/                   # API Gateway (Node.js/Express)
│   ├── editor-service/                # Editor de Niveles (Neo4j)
│   ├── leaderboard-service/           # Leaderboards (Cassandra)
│   ├── wiki-service/                  # Wiki (MongoDB)
│   └── avatar-service/                # Sistema de Avatares (Redis)
│
├── databases/                         # Configuración para bases de datos
│   ├── neo4j/data/                    # Datos persistentes Neo4j
│   ├── cassandra/data/                # Datos persistentes Cassandra
│   ├── mongodb/data/                  # Datos persistentes MongoDB
│   └── redis/data/                    # Datos persistentes Redis
│
└── assets/                            # Recursos para el juego
    └── avatars/                       # Imágenes de avatares
```

## Arquitectura del Sistema

El sistema está compuesto por:

1. **Cuatro bases de datos NoSQL** especializadas
2. **Cuatro servicios API** para cada base de datos
3. **Una API Gateway** centralizada
4. **Cliente Python** para interactuar con todo el sistema

## Descripción de Componentes

### 1. Bases de Datos NoSQL

Cada base de datos se ejecuta en su propio contenedor Docker:

#### Neo4j (Base de Datos de Grafos)
- **Propósito**: Almacenar la estructura de las mazmorras, salas, monstruos y tesoros.
- **Justificación**: Óptima para datos altamente interconectados, ideal para calcular rutas, caminos y relaciones entre entidades del juego.

#### Cassandra (Base de Datos Columnar)
- **Propósito**: Gestionar leaderboards y estadísticas de jugadores.
- **Justificación**: Alto rendimiento para escrituras masivas con escalabilidad horizontal, ideal para registrar constantemente completaciones de mazmorras y asesinatos de monstruos.

#### MongoDB (Base de Datos Documental)
- **Propósito**: Almacenar información de la wiki y comentarios de usuarios.
- **Justificación**: Perfecta para datos semi-estructurados que pueden cambiar con el tiempo, como artículos wiki y comentarios anidados.

#### Redis (Base de Datos Clave-Valor y Vectorial)
- **Propósito**: Sistema de búsqueda de avatares por similitud.
- **Justificación**: Soporte para búsqueda vectorial rápida, ideal para búsqueda por similitud de imágenes y descripciones textuales.

### 2. Servicios API

Cada base de datos tiene su propio servicio API que implementa la lógica específica:

#### Editor Service (Neo4j)
- **Tecnología**: Python con Flask
- **Funcionalidades principales**:
  - Consulta de mazmorras, salas, monstruos y tesoros
  - Cálculo de caminos más cortos entre áreas
  - Búsqueda de elementos por criterios específicos
  - Análisis de enemigos y tesoros en rutas

#### Leaderboard Service (Cassandra)
- **Tecnología**: Python con FastAPI
- **Funcionalidades principales**:
  - Consulta del "Hall of Fame" por mazmorra y país
  - Registro de completaciones de mazmorras
  - Estadísticas de jugadores por años
  - Ranking de eventos de Horda en tiempo real

#### Wiki Service (MongoDB)
- **Tecnología**: Node.js con Express
- **Funcionalidades principales**:
  - Gestión de artículos wiki sobre monstruos, objetos y mazmorras
  - Sistema de comentarios de usuarios
  - Categorización y búsqueda de contenido
  - Notificaciones para QA y PR

#### Avatar Service (Redis)
- **Tecnología**: Python con FastAPI
- **Funcionalidades principales**:
  - Búsqueda de avatares por imagen similar
  - Búsqueda de avatares por descripción textual
  - Almacenamiento y recuperación eficiente de embeddings vectoriales

### 3. API Gateway

- **Tecnología**: Node.js con Express
- **Propósito**: Centralizar todas las peticiones y enrutarlas al servicio adecuado
- **Funcionalidades**:
  - Autenticación y autorización
  - Enrutamiento de solicitudes
  - Balanceo de carga básico
  - Logging y monitoreo

### 4. Cliente Python

- **Propósito**: Proporcionar una interfaz unificada para interactuar con todo el sistema
- **Características**:
  - Métodos específicos para cada servicio
  - Gestión de autenticación
  - Manejo de errores centralizado
  - Ejemplos de uso para cada componente

## Proceso de Desarrollo

### Desarrollo de Bases de Datos NoSQL

#### 1. Neo4j (Base de Datos de Grafos)

**Paso 1: Entender el Modelo de Datos**
- Identificar entidades principales: Areas, Rooms, Monsters, Loot
- Definir relaciones: IS_CONNECTED (entre nodos), CONTAINS (entre Room y Monster/Loot)
- Establecer propiedades para cada tipo de nodo y relación

**Paso 2: Configurar el Contenedor Docker**
```yaml
neo4j:
  image: neo4j:latest
  ports:
    - "7474:7474"  # Interfaz web
    - "7687:7687"  # Protocolo Bolt
  volumes:
    - ./databases/neo4j/data:/data
  environment:
    - NEO4J_AUTH=neo4j/password
```

**Paso 3: Crear Esquema Inicial**
- Desarrollar script Cypher para inicializar el grafo:
```cypher
// Crear restricciones e índices
CREATE CONSTRAINT IF NOT EXISTS FOR (a:Area) REQUIRE a.name IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (r:Room) REQUIRE r.room_id IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (m:Monster) REQUIRE m.id IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (l:Loot) REQUIRE l.id IS UNIQUE;

// Crear índices para búsquedas frecuentes
CREATE INDEX IF NOT EXISTS FOR (r:Room) ON (r.dungeon_name);
CREATE INDEX IF NOT EXISTS FOR (m:Monster) ON (m.level);
```

**Paso 4: Implementar Consultas Cypher Clave**
- Desarrollar las 11 consultas requeridas, por ejemplo:
```cypher
// 1. Buscar salas con un tesoro específico
MATCH (l:Loot {id: $loot_id})<-[:CONTAINS]-(r:Room)
RETURN r.room_id AS id, r.room_name AS name, r.dungeon_name AS dungeon

// 2. Obtener monstruos en una sala
MATCH (r:Room {room_id: $room_id})-[:CONTAINS]->(m:Monster)
RETURN m.id AS id, m.name AS name, m.level AS level, m.type AS type

// 3. Monstruos no presentes en ninguna sala
MATCH (m:Monster)
WHERE NOT (m)<-[:CONTAINS]-()
RETURN m.id AS id, m.name AS name, m.level AS level

// 4. Camino más corto entre áreas
MATCH path = shortestPath((a1:Area {name: $from_area})-[:IS_CONNECTED*]-(a2:Area {name: $to_area}))
RETURN [node in nodes(path) | node.name] AS areas,
       length(path) AS path_length

// 5. Enemigos en el camino más corto
MATCH path = shortestPath((a1:Area {name: $from_area})-[:IS_CONNECTED*]-(a2:Area {name: $to_area}))
UNWIND nodes(path) AS area_node
MATCH (area_node)<-[:IS_CONNECTED]-(r:Room)-[:CONTAINS]->(m:Monster)
RETURN DISTINCT m.id AS id, m.name AS name, m.level AS level, r.room_id AS room_id

// 6 al 11: Implementar las demás consultas requeridas
```

**Paso 5: Implementar API Flask**
- Crear servicios y rutas para exponer la funcionalidad a través de API REST
- Implementar métodos para ejecutar las consultas Cypher y transformar los resultados
- Añadir documentación y manejo de errores

#### 2. Cassandra (Base de Datos Columnar)

**Paso 1: Diseñar el Modelo de Datos**
- Analizar patrones de acceso: Hall of Fame, estadísticas de jugador, ranking de Horda
- Diseñar tablas optimizadas para patrones de consulta específicos
- Considerar particionamiento, TTL y niveles de consistencia

**Paso 2: Configurar el Contenedor Docker**
```yaml
cassandra:
  image: cassandra:latest
  ports:
    - "9042:9042"
  volumes:
    - ./databases/cassandra/data:/var/lib/cassandra
  environment:
    - MAX_HEAP_SIZE=512M
    - HEAP_NEWSIZE=100M
```

**Paso 3: Crear Esquema CQL**
```cql
-- Keyspace del juego
CREATE KEYSPACE IF NOT EXISTS jotun_lair
WITH REPLICATION = {
  'class': 'SimpleStrategy',
  'replication_factor': 3
};

USE jotun_lair;

-- Tabla para Hall of Fame
CREATE TABLE IF NOT EXISTS hall_of_fame (
  country text,
  dungeon_id int,
  year int,
  month int,
  email text,
  user_name text,
  minutes float,
  date timestamp,
  PRIMARY KEY ((country, dungeon_id, year, month), minutes, email)
) WITH CLUSTERING ORDER BY (minutes ASC);

-- Tabla para estadísticas de jugador
CREATE TABLE IF NOT EXISTS player_stats (
  email text,
  year int,
  dungeon_id int,
  avg_minutes float,
  PRIMARY KEY ((email, year), dungeon_id)
);

-- Tabla para ranking de Horda
CREATE TABLE IF NOT EXISTS horde_ranking (
  event_id int,
  country text,
  user_id int,
  user_name text,
  email text,
  n_killed int,
  PRIMARY KEY ((event_id, country), n_killed, user_id)
) WITH CLUSTERING ORDER BY (n_killed DESC);
```

**Paso 4: Implementar Servicio Cassandra**
```python
# services/cassandra_service.py
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.query import SimpleStatement

class CassandraService:
    def __init__(self, contact_points, port, keyspace):
        self.cluster = Cluster(contact_points.split(','), port=port)
        self.session = self.cluster.connect(keyspace)
        
    # Métodos para Hall of Fame
    async def get_hall_of_fame(self, country, dungeon_id, consistency_level=None):
        query = SimpleStatement(
            "SELECT email, user_name, minutes, date FROM hall_of_fame " +
            "WHERE country = %s AND dungeon_id = %s AND year = %s AND month = %s " +
            "LIMIT 5",
            consistency_level=consistency_level
        )
        
        # Obtener año y mes actuales para filtrado
        # Solo mostrar datos de los últimos 4 meses
        current_year, current_month = self._get_current_year_month()
        months = self._get_past_four_months(current_year, current_month)
        
        results = []
        for year, month in months:
            rows = await self.session.execute_async(query, (country, dungeon_id, year, month))
            results.extend(rows)
            
        # Ordenar por minutos (ascendente) y tomar top 5
        results.sort(key=lambda x: x['minutes'])
        return results[:5]
    
    # Método para registrar completación de mazmorra
    async def record_dungeon_completion(self, email, dungeon_id, minutes, date, consistency_level=None):
        # Implementar lógica para registrar completación y actualizar estadísticas
        pass
        
    # Métodos para ranking de Horda
    async def get_horde_ranking(self, country, event_id, consistency_level=None):
        # Implementar lógica para obtener ranking de Horda
        pass
```

**Paso 5: Implementar API FastAPI**
- Crear endpoints REST para todas las funcionalidades requeridas
- Implementar diferentes niveles de consistencia según los requerimientos
- Añadir validación de datos y manejo de errores

#### 3. MongoDB (Base de Datos Documental)

**Paso 1: Diseñar Esquema Flexible**
- Definir colecciones: Rooms, Users, Monsters, Loot
- Decidir entre modelo embebido o normalizado para comentarios
- Diseñar índices para consultas frecuentes

**Paso 2: Configurar el Contenedor Docker**
```yaml
mongodb:
  image: mongo:latest
  ports:
    - "27017:27017"
  volumes:
    - ./databases/mongodb/data:/data/db
  environment:
    - MONGO_INITDB_DATABASE=jotun_wiki
```

**Paso 3: Crear Colecciones e Índices**
```javascript
// Inicializar colecciones
db.createCollection("rooms");
db.createCollection("users");
db.createCollection("monsters");
db.createCollection("loot");

// Crear índices
db.rooms.createIndex({ room_id: 1 }, { unique: true });
db.rooms.createIndex({ dungeon_id: 1 });
db.rooms.createIndex({ "hints.category": 1 });
db.users.createIndex({ email: 1 }, { unique: true });
db.monsters.createIndex({ id: 1 }, { unique: true });
db.loot.createIndex({ id: 1 }, { unique: true });
```

**Paso 4: Implementar Modelos Mongoose**
```javascript
// models/room.js
const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const RoomSchema = new Schema({
  room_id: {
    type: Number,
    required: true,
    unique: true
  },
  room_name: {
    type: String,
    required: true
  },
  dungeon_id: {
    type: Number,
    required: true
  },
  dungeon_name: {
    type: String,
    required: true
  },
  in_waypoint: String,
  out_waypoint: String,
  rooms_connected: [{
    room_id: Number,
    room_name: String
  }],
  hints: [{
    creation_date: String,
    text: String,
    category: {
      type: String,
      enum: ['Bug', 'Hint', 'Lore', 'Suggestion']
    },
    publish_by: {
      email: String,
      user_name: String,
      creation_date: String,
      country: String
    }
  }],
  monsters: [{
    id: Number,
    name: String,
    place: String,
    type: String,
    man_page: Number,
    level: Number,
    exp: Number
  }],
  loot: [{
    id: Number,
    name: String,
    type1: String,
    type2: String,
    weight: String,
    gold: Number
  }]
});
```

**Paso 5: Implementar Controladores y Rutas Express**
```javascript
// controllers/room.js
const Room = require('../models/room');

exports.getRoomById = async (req, res, next) => {
  try {
    const { room_id } = req.params;
    
    // Convert string to number
    const roomIdNum = parseInt(room_id, 10);
    if (isNaN(roomIdNum)) {
      return res.status(400).json({ error: 'Invalid room ID' });
    }
    
    const room = await Room.findOne({ room_id: roomIdNum });
    
    if (!room) {
      return res.status(404).json({ error: 'Room not found' });
    }
    
    return res.json({
      room_id: room.room_id,
      name: room.room_name,
      inWP: room.in_waypoint,
      outWP: room.out_waypoint,
      dungeon_id: room.dungeon_id,
      dungeon_name: room.dungeon_name,
      monsters: room.monsters,
      loot: room.loot,
      hints: room.hints
    });
  } catch (error) {
    next(error);
  }
};

// Implementar otros controladores para POST /comment, etc.
```

**Paso 6: Implementar API REST Completa**
- Definir todas las rutas requeridas
- Implementar autenticación para endpoints privados
- Añadir validación y manejo de errores

#### 4. Redis (Base de Datos Clave-Valor y Vectorial)

**Paso 1: Preparar el Modelo de Vectores**
- Seleccionar modelo CLIP para generación de embeddings
- Definir formato de almacenamiento para avatares y sus metadatos
- Decidir estructura para índices vectoriales

**Paso 2: Configurar el Contenedor Docker**
```yaml
redis:
  image: redis/redis-stack:latest
  ports:
    - "6379:6379"  # Redis core
    - "8001:8001"  # RedisInsight
  volumes:
    - ./databases/redis/data:/data
```

**Paso 3: Configurar Índices Vectoriales**
```
FT.CREATE avatar_idx ON HASH PREFIX 1 avatar:
SCHEMA avatar_id TEXT
       filename TEXT
       gender TEXT
       race TEXT
       job TEXT
       age NUMERIC
       embedding VECTOR HNSW 6 TYPE FLOAT32 DIM 512 DISTANCE_METRIC COSINE
```

**Paso 4: Implementar Servicio de Embeddings**
```python
# services/embedding_service.py
import torch
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import numpy as np
import io

class EmbeddingService:
    def __init__(self):
        self.model = None
        self.processor = None
        
    def initialize(self):
        """Initialize CLIP model and processor"""
        self.model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        self.processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
        print("CLIP model initialized")
        
    def get_image_embedding(self, image_data):
        """Get embedding for an image"""
        if isinstance(image_data, str):
            # Image path
            image = Image.open(image_data).convert("RGB")
        elif isinstance(image_data, bytes):
            # Image bytes
            image = Image.open(io.BytesIO(image_data)).convert("RGB")
        else:
            # PIL Image
            image = image_data
            
        # Process image
        inputs = self.processor(images=image, return_tensors="pt", padding=True)
        
        # Get embedding
        with torch.no_grad():
            image_features = self.model.get_image_features(**inputs)
            
        # Normalize embedding
        image_embedding = image_features.squeeze().numpy().astype(np.float32)
        image_embedding = image_embedding / np.linalg.norm(image_embedding)
        
        return image_embedding
        
    def get_text_embedding(self, text):
        """Get embedding for text description"""
        # Process text
        inputs = self.processor(text=text, return_tensors="pt", padding=True)
        
        # Get embedding
        with torch.no_grad():
            text_features = self.model.get_text_features(**inputs)
            
        # Normalize embedding
        text_embedding = text_features.squeeze().numpy().astype(np.float32)
        text_embedding = text_embedding / np.linalg.norm(text_embedding)
        
        return text_embedding
```

**Paso 5: Implementar Servicio Redis**
```python
# services/redis_service.py
import redis
from redis.commands.search.field import VectorField, TextField, NumericField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
import numpy as np

class RedisService:
    def __init__(self, host="localhost", port=6379, password=None):
        self.host = host
        self.port = port
        self.password = password
        self.client = None
        
    async def connect(self):
        """Connect to Redis"""
        self.client = redis.Redis(
            host=self.host,
            port=self.port,
            password=self.password,
            decode_responses=False  # Required for binary data
        )
        # Test connection
        self.client.ping()
        print(f"Connected to Redis at {self.host}:{self.port}")
        
    async def close(self):
        """Close Redis connection"""
        if self.client:
            self.client.close()
            print("Redis connection closed")
            
    async def create_index(self):
        """Create vector index for avatar embeddings"""
        schema = [
            TextField("avatar_id"),
            TextField("filename"),
            TextField("gender"),
            TextField("race"),
            TextField("job"),
            NumericField("age"),
            VectorField("embedding", 
                       "HNSW", 
                       {"TYPE": "FLOAT32", 
                        "DIM": 512,  # CLIP embedding dimension
                        "DISTANCE_METRIC": "COSINE",
                        "M": 40,
                        "EF_CONSTRUCTION": 200})
        ]
        
        try:
            # Create index if it doesn't exist
            self.client.ft().create_index(
                schema, 
                definition=IndexDefinition(
                    prefix=["avatar:"], 
                    index_type=IndexType.HASH
                )
            )
            print("Vector index created")
        except redis.exceptions.ResponseError as e:
            # Index already exists
            if "Index already exists" in str(e):
                print("Index already exists")
            else:
                raise
                
    async def store_avatar(self, avatar_id, filename, gender, race, job, age, embedding):
        """Store avatar with embedding in Redis"""
        # Convert embedding to bytes
        embedding_bytes = embedding.astype(np.float32).tobytes()
        
        # Store in Redis
        self.client.hset(
            f"avatar:{avatar_id}",
            mapping={
                "avatar_id": str(avatar_id),
                "filename": filename,
                "gender": gender,
                "race": race,
                "job": job,
                "age": str(age),
                "embedding": embedding_bytes
            }
        )
        
    async def find_similar_avatars(self, embedding, top_k=5):
        """Find avatars similar to the given embedding"""
        # Convert embedding to bytes
        embedding_bytes = embedding.astype(np.float32).tobytes()
        
        # Search query
        query = f"*=>[KNN {top_k} @embedding $embedding]"
        params = {"embedding": embedding_bytes}
        
        # Execute search
        results = self.client.ft().search(query, params).docs
        
        # Process results
        avatars = []
        for res in results:
            avatars.append({
                "id": res["avatar_id"],
                "filename": res["filename"],
                "gender": res["gender"],
                "race": res["race"],
                "job": res["job"],
                "age": int(res["age"]),
                "similarity": 1.0 - float(res["__embedding_score"])  # Convert score to similarity
            })
            
        return avatars
```

**Paso 6: Implementar API FastAPI**
- Crear endpoints para búsqueda por imagen y texto
- Implementar carga y procesamiento de imágenes
- Añadir validación y documentación

### Desarrollo de API Gateway

**Paso 1: Configurar Entorno Node.js**
- Configurar proyecto Express.js básico
- Instalar dependencias necesarias
- Definir estructura de carpetas y archivos

**Paso 2: Implementar Configuración**
```javascript
// config.js
module.exports = {
  services: {
    editor: {
      url: process.env.EDITOR_SERVICE_URL || 'http://editor-service:8080'
    },
    leaderboard: {
      url: process.env.LEADERBOARD_SERVICE_URL || 'http://leaderboard-service:8080'
    },
    wiki: {
      url: process.env.WIKI_SERVICE_URL || 'http://wiki-service:8080'
    },
    avatar: {
      url: process.env.AVATAR_SERVICE_URL || 'http://avatar-service:8080'
    }
  },
  auth: {
    jwtSecret: process.env.JWT_SECRET || 'your-secret-key',
    tokenExpiration: process.env.TOKEN_EXPIRATION || '24h'
  }
};
```

**Paso 3: Implementar Middleware de Autenticación**
```javascript
// middlewares/auth.js
const jwt = require('jsonwebtoken');
const config = require('../config');

exports.authenticate = (req, res, next) => {
  const token = req.header('x-auth-token');
  
  if (!token) {
    return res.status(401).json({ error: 'No token, authorization denied' });
  }
  
  try {
    const decoded = jwt.verify(token, config.auth.jwtSecret);
    req.user = decoded.user;
    next();
  } catch (err) {
    res.status(401).json({ error: 'Token is not valid' });
  }
};

exports.verifyAdmin = (req, res, next) => {
  if (!req.user || !req.user.isAdmin) {
    return res.status(403).json({ error: 'Access denied. Admin privileges required' });
  }
  next();
};
```

**Paso 4: Implementar Enrutamiento**
```javascript
// index.js
const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const { createProxyMiddleware } = require('http-proxy-middleware');

const config = require('./config');
const authMiddleware = require('./middlewares/auth');

// Initialize Express app
const app = express();

// Middlewares
app.use(helmet());
app.use(cors());
app.use(express.json());

// Health check endpoint
app.get('/health', (req, res) => {
  res.status(200).json({ status: 'ok' });
});

// Authentication middleware for protected routes
app.use('/api/editor', authMiddleware.authenticate);
app.use('/api/leaderboard/halloffame/record-completion', authMiddleware.authenticate);
app.use('/api/leaderboard/horde/record-kill', authMiddleware.authenticate);
app.use('/api/wiki/comment', authMiddleware.authenticate);

// Define routes based on configuration
app.use('/api/editor', createProxyMiddleware({
  target: config.services.editor.url,
  changeOrigin: true,
  pathRewrite: { '^/api/editor': '/' },
}));

app.use('/api/leaderboard', createProxyMiddleware({
  target: config.services.leaderboard.url,
  changeOrigin: true,
  pathRewrite: { '^/api/leaderboard': '/' },
}));

app.use('/api/wiki', createProxyMiddleware({
  target: config.services.wiki.url,
  changeOrigin: true,
  pathRewrite: { '^/api/wiki': '/api' },
}));

app.use('/api/avatar', createProxyMiddleware({
  target: config.services.avatar.url,
  changeOrigin: true,
  pathRewrite: { '^/api/avatar': '/' },
}));

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err);
  res.status(500).json({ error: 'Internal server error' });
});

// Start server
const PORT = process.env.PORT || 8080;
app.listen(PORT, () => {
  console.log(`API Gateway running on port ${PORT}`);
});
```

### Desarrollo del Cliente Python

**Paso 1: Diseñar Estructura del Cliente**
- Definir estructura de clases y métodos
- Planificar manejo de errores y autenticación
- Preparar entorno de desarrollo Python

**Paso 2: Implementar Cliente Base**
```python
# jotun_client.py
import requests
import json
from typing import Dict, List, Optional, Union, Any
import os
from datetime import datetime
import logging

class JotunLairClient:
    """
    Cliente Python para interactuar con el API Gateway del sistema "The Jötun's Lair".
    Proporciona métodos para acceder a todas las funcionalidades de los distintos servicios:
    - Editor de Niveles (Neo4j)
    - Leaderboards (Cassandra)
    - Wiki (MongoDB)
    - Sistema de Avatares (Redis)
    """
    
    def __init__(self, base_url="http://localhost:8080/api", token=None):
        """
        Inicializa el cliente con la URL base del API Gateway y un token opcional.
        
        Args:
            base_url: URL base del API Gateway
            token: Token JWT para autenticación
        """
        self.base_url = base_url
        self.token = token
        self.session = requests.Session()
        
        # Configurar logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            filename='jotun_client.log'
        )
        self.logger = logging.getLogger('JotunLairClient')
        
        # Si hay token, configurar los headers
        if token:
            self.session.headers.update({"x-auth-token": token})
    
    def authenticate(self, email: str, password: str) -> bool:
        """
        Autenticar al usuario y obtener un token JWT.
        
        Args:
            email: Email del usuario
            password: Contraseña del usuario
            
        Returns:
            bool: True si la autenticación fue exitosa
        """
        try:
            response = self.session.post(
                f"{self.base_url}/auth/login",
                json={"email": email, "password": password}
            )
            response.raise_for_status()
            
            data = response.json()
            self.token = data.get("token")
            
            if self.token:
                self.session.headers.update({"x-auth-token": self.token})
                self.logger.info(f"Usuario {email} autenticado correctamente")
                return True
            
            return False
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error de autenticación: {str(e)}")
            return False
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict:
        """
        Método interno para realizar peticiones HTTP.
        
        Args:
            method: Método HTTP (GET, POST, PUT, DELETE)
            endpoint: Endpoint de la API
            **kwargs: Argumentos adicionales para la petición
            
        Returns:
            Dict: Respuesta JSON de la API
            
        Raises:
            Exception: Si la petición falla
        """
        url = f"{self.base_url}/{endpoint}"
        
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            
            if response.content:
                return response.json()
            return {"status": "success"}
            
        except requests.exceptions.HTTPError as e:
            self.logger.error(f"Error HTTP: {str(e)}")
            if response.content:
                error_data = response.json()
                self.logger.error(f"Detalles del error: {error_data}")
                raise Exception(f"Error API: {error_data.get('error', str(e))}")
            raise Exception(f"Error HTTP: {str(e)}")
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error de petición: {str(e)}")
            raise Exception(f"Error de conexión: {str(e)}")
```

**Paso 3: Implementar Métodos para Editor de Niveles**
```python
# Métodos para Editor de Niveles (Neo4j)
def get_areas(self) -> List[Dict]:
    """Obtener todas las áreas del juego"""
    return self._make_request("GET", "editor/areas")

def get_area_by_name(self, name: str) -> Dict:
    """Obtener área por nombre"""
    return self._make_request("GET", f"editor/areas/{name}")

def get_dungeon_by_id(self, dungeon_id: int) -> Dict:
    """Obtener mazmorra por ID"""
    return self._make_request("GET", f"editor/dungeons/{dungeon_id}")

def get_all_dungeons(self) -> List[Dict]:
    """Obtener todas las mazmorras"""
    return self._make_request("GET", "editor/dungeons")

def get_room_by_id(self, room_id: int) -> Dict:
    """Obtener habitación por ID"""
    return self._make_request("GET", f"editor/rooms/{room_id}")

def get_rooms_with_loot(self, loot_id: int) -> List[Dict]:
    """Buscar todas las salas que contienen un tesoro específico"""
    return self._make_request("GET", f"editor/loots/{loot_id}/rooms")

def get_monsters_in_room(self, room_id: int) -> List[Dict]:
    """Obtener todos los monstruos en una sala"""
    return self._make_request("GET", f"editor/rooms/{room_id}/monsters")

def get_unused_monsters(self) -> List[Dict]:
    """Obtener todos los monstruos que no están en ninguna sala"""
    return self._make_request("GET", "editor/monsters/unused")

def get_shortest_path(self, from_area: str, to_area: str) -> Dict:
    """Calcular el camino más corto entre dos áreas"""
    return self._make_request(
        "GET", 
        "editor/paths/shortest",
        params={"from": from_area, "to": to_area}
    )

def get_enemies_in_path(self, from_area: str, to_area: str) -> List[Dict]:
    """Obtener los enemigos en el camino más corto entre dos áreas"""
    return self._make_request(
        "GET", 
        "editor/paths/enemies",
        params={"from": from_area, "to": to_area}
    )

def get_areas_in_path(self, from_area: str, to_area: str) -> List[str]:
    """Obtener las áreas en el camino entre dos áreas"""
    return self._make_request(
        "GET", 
        "editor/paths/areas",
        params={"from": from_area, "to": to_area}
    )

def create_area_connections(self) -> Dict:
    """Crear conexiones directas entre áreas conectadas por mazmorras"""
    return self._make_request("POST", "editor/areas/connections")

def get_world_map(self) -> Dict:
    """Obtener el mapamundi del juego"""
    return self._make_request("GET", "editor/worldmap")

def get_dungeon_gold(self, dungeon_id: int) -> Dict:
    """Calcular el total de oro en una mazmorra"""
    return self._make_request("GET", f"editor/dungeons/{dungeon_id}/gold")

def get_high_level_monsters(self, dungeon_id: int) -> List[Dict]:
    """Obtener las salas con los monstruos de más alto nivel de una mazmorra"""
    return self._make_request("GET", f"editor/dungeons/{dungeon_id}/high-level-monsters")

def get_encounters_by_exp(self, dungeon_id: int) -> List[Dict]:
    """Obtener los encuentros ordenados por experiencia en una mazmorra"""
    return self._make_request("GET", f"editor/dungeons/{dungeon_id}/encounters")
```

**Paso 4: Implementar Métodos para Leaderboards**
```python
# Métodos para Leaderboards (Cassandra)
def get_hall_of_fame(self, country: str, dungeon_id: int) -> Dict:
    """Obtener el Hall of Fame para una mazmorra y país"""
    return self._make_request(
        "GET", 
        "leaderboard/halloffame",
        params={"country": country, "dungeon_id": dungeon_id}
    )

def record_dungeon_completion(self, email: str, dungeon_id: int, 
                             time_minutes: float, date: str) -> Dict:
    """Registrar la completación de una mazmorra"""
    return self._make_request(
        "POST", 
        "leaderboard/halloffame/record-completion",
        json={
            "email": email, 
            "dungeon_id": dungeon_id,
            "time_minutes": time_minutes, 
            "date": date
        }
    )

def get_player_stats(self, email: str, year: int) -> Dict:
    """Obtener estadísticas de un jugador para un año"""
    return self._make_request(
        "GET", 
        "leaderboard/statistics",
        params={"email": email, "year": year}
    )

def get_horde_ranking(self, country: str, event_id: int) -> Dict:
    """Obtener ranking de un evento de Horda"""
    return self._make_request(
        "GET", 
        "leaderboard/horde/ranking",
        params={"country": country, "event_id": event_id}
    )

def record_monster_kill(self, email: str, event_id: int, monster_id: int) -> Dict:
    """Registrar la muerte de un monstruo en un evento de Horda"""
    return self._make_request(
        "POST", 
        "leaderboard/horde/record-kill",
        json={
            "email": email, 
            "event_id": event_id, 
            "monster_id": monster_id
        }
    )
```

**Paso 5: Implementar Métodos para Wiki**
```python
# Métodos para Wiki (MongoDB)
def get_all_loots(self) -> List[Dict]:
    """Obtener todos los objetos del juego"""
    return self._make_request("GET", "wiki/loot")

def get_loot_by_id(self, loot_id: int) -> Dict:
    """Obtener información detallada de un objeto"""
    return self._make_request("GET", f"wiki/loot/{loot_id}")

def get_all_monsters(self) -> List[Dict]:
    """Obtener todos los monstruos del juego"""
    return self._make_request("GET", "wiki/monster")

def get_monster_by_id(self, monster_id: int) -> Dict:
    """Obtener información detallada de un monstruo"""
    return self._make_request("GET", f"wiki/monster/{monster_id}")

def get_all_dungeons_wiki(self) -> List[Dict]:
    """Obtener todas las mazmorras (versión wiki)"""
    return self._make_request("GET", "wiki/dungeon")

def get_dungeon_wiki(self, dungeon_id: int) -> Dict:
    """Obtener información detallada de una mazmorra para la wiki"""
    return self._make_request("GET", f"wiki/dungeon/{dungeon_id}")

def get_room_wiki(self, room_id: int) -> Dict:
    """Obtener información detallada de una habitación para la wiki"""
    return self._make_request("GET", f"wiki/room/{room_id}")

def get_all_users(self) -> List[Dict]:
    """Obtener todos los usuarios"""
    return self._make_request("GET", "wiki/user")

def get_user_by_email(self, email: str) -> Dict:
    """Obtener información de un usuario y sus comentarios"""
    return self._make_request("GET", f"wiki/user/{email}")

def add_comment(self, user_email: str, room_id: int, text: str, category: str) -> Dict:
    """Añadir un comentario a una habitación"""
    return self._make_request(
        "POST", 
        "wiki/comment",
        json={
            "user_email": user_email, 
            "room_id": room_id,
            "text": text, 
            "category": category
        }
    )
```

**Paso 6: Implementar Métodos para Sistema de Avatares**
```python
# Métodos para Sistema de Avatares (Redis)
def search_avatar_by_image(self, image_path: str, top_k: int = 5) -> List[Dict]:
    """
    Buscar avatares similares a una imagen
    
    Args:
        image_path: Ruta al archivo de imagen
        top_k: Número de resultados a devolver
        
    Returns:
        List[Dict]: Lista de avatares similares
    """
    try:
        with open(image_path, 'rb') as image_file:
            files = {'file': (os.path.basename(image_path), image_file, 'image/jpeg')}
            response = self.session.post(
                f"{self.base_url}/avatar/search/image",
                files=files,
                data={'top_k': top_k}
            )
            response.raise_for_status()
            return response.json()
    except Exception as e:
        self.logger.error(f"Error al buscar avatar por imagen: {str(e)}")
        raise Exception(f"Error al buscar avatar por imagen: {str(e)}")

def search_avatar_by_text(self, description: str, top_k: int = 5) -> List[Dict]:
    """
    Buscar avatares que coincidan con una descripción textual
    
    Args:
        description: Descripción textual del avatar
        top_k: Número de resultados a devolver
        
    Returns:
        List[Dict]: Lista de avatares similares
    """
    try:
        response = self.session.post(
            f"{self.base_url}/avatar/search/text",
            data={'description': description, 'top_k': top_k}
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        self.logger.error(f"Error al buscar avatar por texto: {str(e)}")
        raise Exception(f"Error al buscar avatar por texto: {str(e)}")
```

## Docker Compose para Despliegue

A continuación se presenta el archivo `docker-compose.yml` completo para desplegar todo el sistema:

```yaml
version: '3.8'

services:
  # Bases de datos
  neo4j:
    image: neo4j:latest
    ports:
      - "7474:7474"  # Interfaz web
      - "7687:7687"  # Protocolo Bolt
    volumes:
      - ./databases/neo4j/data:/data
    environment:
      - NEO4J_AUTH=neo4j/password

  cassandra:
    image: cassandra:latest
    ports:
      - "9042:9042"
    volumes:
      - ./databases/cassandra/data:/var/lib/cassandra
    environment:
      - MAX_HEAP_SIZE=512M
      - HEAP_NEWSIZE=100M

  mongodb:
    image: mongo:latest
    ports:
      - "27017:27017"
    volumes:
      - ./databases/mongodb/data:/data/db
    environment:
      - MONGO_INITDB_DATABASE=jotun_wiki

  redis:
    image: redis/redis-stack:latest
    ports:
      - "6379:6379"  # Redis core
      - "8001:8001"  # RedisInsight
    volumes:
      - ./databases/redis/data:/data

  # Servicios de aplicación
  editor-service:
    build: ./services/editor-service
    depends_on:
      - neo4j
    ports:
      - "8081:8080"
    environment:
      - NEO4J_URI=bolt://neo4j:7687
      - NEO4J_USER=neo4j
      - NEO4J_PASSWORD=password
    volumes:
      - ./services/editor-service:/app
      - /app/node_modules

  leaderboard-service:
    build: ./services/leaderboard-service
    depends_on:
      - cassandra
    ports:
      - "8082:8080"
    environment:
      - CASSANDRA_CONTACT_POINTS=cassandra:9042
    volumes:
      - ./services/leaderboard-service:/app
      - /app/node_modules

  wiki-service:
    build: ./services/wiki-service
    depends_on:
      - mongodb
    ports:
      - "8083:8080"
    environment:
      - MONGODB_URI=mongodb://mongodb:27017/jotun_wiki
    volumes:
      - ./services/wiki-service:/app
      - /app/node_modules

  avatar-service:
    build: ./services/avatar-service
    depends_on:
      - redis
    ports:
      - "8084:8080"
    environment:
      - REDIS_HOST=redis
      - REDIS_PORT=6379
    volumes:
      - ./services/avatar-service:/app
      - ./assets/avatars:/app/assets/avatars
      - /app/node_modules

  # API Gateway
  api-gateway:
    build: ./services/api-gateway
    ports:
      - "8080:8080"
    depends_on:
      - editor-service
      - leaderboard-service
      - wiki-service
      - avatar-service
    environment:
      - EDITOR_SERVICE_URL=http://editor-service:8080
      - LEADERBOARD_SERVICE_URL=http://leaderboard-service:8080
      - WIKI_SERVICE_URL=http://wiki-service:8080
      - AVATAR_SERVICE_URL=http://avatar-service:8080
      - JWT_SECRET=your-secret-key
    volumes:
      - ./services/api-gateway:/app
      - /app/node_modules

volumes:
  neo4j_data:
  cassandra_data:
  mongo_data:
  redis_data:
```

## Instrucciones de Despliegue

### 1. Prerequisitos

- Docker y Docker Compose instalados
- Git para clonar el repositorio
- Python 3.8+ para ejecutar el cliente
- Mínimo 8GB de RAM para ejecutar todos los servicios

### 2. Configuración Inicial

```bash
# Clonar el repositorio
git clone https://github.com/your-organization/Norsewind_Studio.git
cd Norsewind_Studio

# Crear volúmenes para datos persistentes
mkdir -p databases/neo4j/data
mkdir -p databases/cassandra/data
mkdir -p databases/mongodb/data
mkdir -p databases/redis/data
```

### 3. Iniciar los Servicios

```bash
# Iniciar todos los servicios
docker-compose up -d

# Verificar que todos los servicios estén corriendo
docker-compose ps
```

### 4. Probar el Sistema

```bash
# Instalar dependencias del cliente
cd client
pip install -r requirements.txt

# Ejecutar ejemplo para probar el editor de niveles
python examples/editor_examples.py
```

## Comunicación entre Servicios

El sistema está diseñado para permitir la comunicación entre servicios cuando sea necesario. Esto ocurre a través del API Gateway, que puede:

1. **Enrutar peticiones directamente** a un servicio específico
2. **Agregar datos de múltiples servicios** para peticiones complejas
3. **Transmitir eventos** entre servicios cuando se requiera

### Ejemplo: Actualización de Rankings al Completar una Mazmorra

Cuando un jugador completa una mazmorra, se puede registrar a través del API Gateway:

1. El cliente Python envía la información de completación al API Gateway
2. El Gateway reenvía la información al Leaderboard Service
3. El Leaderboard Service actualiza los rankings
4. Opcionalmente, el Gateway puede notificar al Wiki Service para registrar un logro o actualizar estadísticas

## Conclusiones

Este proyecto demuestra la selección e implementación de bases de datos NoSQL específicas según las necesidades de cada componente de un sistema complejo. Al elegir la base de datos adecuada para cada caso de uso, aprovechamos sus fortalezas específicas:

- **Neo4j** para datos altamente relacionales y búsqueda de rutas
- **Cassandra** para escrituras masivas y alta disponibilidad
- **MongoDB** para datos flexibles y anidados
- **Redis** para búsquedas vectoriales de alta velocidad

La arquitectura de microservicios con un API Gateway centralizado proporciona flexibilidad, escalabilidad y facilidad de mantenimiento, permitiendo que cada componente evolucione independientemente.
