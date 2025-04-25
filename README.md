# The Jötun's Lair - Sistema de Bases de Datos NoSQL

Este repositorio contiene el sistema de backend del videojuego **"The Jötun's Lair"**, implementado con una arquitectura de microservicios que utiliza distintas bases de datos NoSQL especializadas según las necesidades de cada componente:

- **Neo4j (grafos)**: Editor de niveles y mazmorras  
- **Cassandra (columnar)**: Sistema de rankings y leaderboards  
- **MongoDB (documentos)**: Wiki del juego  
- **Redis (clave-valor + vectorial)**: Recomendación de avatares

---

## 🔁 Clonar el repositorio

```bash
git clone https://github.com/Solrac1388/Norsewind_Studio.git 
```

---

## 🚀 Iniciar el sistema

Ejecuta todo el sistema con Docker Compose:

```bash
docker-compose up --build -d
```

### Servicios y puertos:

| Servicio            | Puerto(s)                                      |
|---------------------|------------------------------------------------|
| Neo4j               | 7474 (web), 7687 (Bolt)                        |
| Cassandra           | 9042                                           |
| MongoDB             | 27017                                          |
| Redis/RedisInsight  | 6379 (Redis), 8001 (Insight)                   |
| Editor Service      | 8081                                           |
| Leaderboard Service | 8082                                           |
| Wiki Service        | 8083                                           |
| Avatar Service      | 8084                                           |

---

## 🧪 Consultas por servicio (`curl`)

### 📌 Editor Service (Neo4j)

```bash
# Buscar salas con un loot específico
curl -X GET "http://localhost:8081/api/editor/loots/1/rooms"

# Monstruos en una sala
curl -X GET "http://localhost:8081/api/editor/rooms/1/monsters"

# Monstruos sin sala asignada
curl -X GET "http://localhost:8081/api/editor/monsters/unused"

# Camino más corto entre áreas
curl -X GET "http://localhost:8081/api/editor/paths/shortest?from=Jolly%20Steppe%20of%20Emerald%20city&to=Uptight%20Shrubland%20of%20Avalon"

# Enemigos entre dos áreas
curl -X GET "http://localhost:8081/api/editor/paths/enemies?from=Jolly%20Steppe%20of%20Emerald%20city&to=Uptight%20Shrubland%20of%20Avalon"

# Áreas a recorrer entre zonas
curl -X GET "http://localhost:8081/api/editor/paths/areas?from=Jolly%20Steppe%20of%20Emerald%20city&to=Uptight%20Shrubland%20of%20Avalon"

# Crear conexión entre áreas
curl -X POST "http://localhost:8081/api/editor/areas/connections"

# Mostrar el mapamundi
curl -X GET "http://localhost:8081/api/editor/worldmap"

# Total de oro en una mazmorra
curl -X GET "http://localhost:8081/api/editor/dungeons/Bentclock%2C%20Laboratory%20of%20the%20Sexy%20Thieves/gold"

# Salas con monstruos de alto nivel
curl -X GET "http://localhost:8081/api/editor/dungeons/Bentclock%2C%20Laboratory%20of%20the%20Sexy%20Thieves/high-level-monsters"

# Experiencia de encuentros
curl -X GET "http://localhost:8081/api/editor/dungeons/Bentclock%2C%20Laboratory%20of%20the%20Sexy%20Thieves/encounters"
```

### 🏆 Leaderboard Service (Cassandra)

```bash
# Estadísticas por jugador
curl -X GET "http://localhost:8082/statistics?email=player@example.com&year=2023"

# Hall of Fame por mazmorra
curl -X GET "http://localhost:8082/halloffame?country=spain&dungeon_id=1"

# Ranking por evento Horda
curl -X GET "http://localhost:8082/horde/ranking?country=spain&event_id=101"

# Registrar completado de mazmorra
curl -X POST "http://localhost:8082/halloffame/record-completion"   -H "Content-Type: application/json"   -d '{"email": "player@example.com", "dungeon_id": 1, "time_minutes": 45.5, "date": "2023-04-25T14:30:00"}'

# Registrar baja en evento Horda
curl -X POST "http://localhost:8082/horde/record-kill"   -H "Content-Type: application/json"   -d '{"email": "player@example.com", "event_id": 101, "monster_id": 2}'
```

### 📚 Wiki Service (MongoDB)

```bash
# Mazmorras
curl -X GET "http://localhost:8083/dungeon"
curl -X GET "http://localhost:8083/dungeon/1"

# Objetos
curl -X GET "http://localhost:8083/loot"
curl -X GET "http://localhost:8083/loot/1"

# Monstruos
curl -X GET "http://localhost:8083/monster"
curl -X GET "http://localhost:8083/monster/1"

# Sala y comentarios
curl -X GET "http://localhost:8083/room/1"

# Añadir comentario
curl -X POST "http://localhost:8083/room/comment"   -H "Content-Type: application/json"   -d '{"user_email": "user@example.com", "room_id": 1, "text": "Comentario de prueba", "category": "Hint"}'

# Eliminar monstruo
curl -X DELETE "http://localhost:8083/monster/1"
```

### 🧬 Avatar Service (Redis)

```bash
# Buscar por descripción
curl -X POST "http://localhost:8084/search/text"   -F "description=Guerrero elfo con armadura plateada"   -F "top_k=5"

# Buscar por imagen
curl -X POST "http://localhost:8084/search/image"   -F "file=@ruta/a/tu/imagen.jpg"   -F "top_k=5"

# Health check
curl -X GET "http://localhost:8084/health"
```

---

## ⚠️ Limitaciones conocidas

- **Integración parcial entre servicios**: El API Gateway existe pero algunas rutas aún no están conectadas.
- **Autenticación incompleta**: Stubs presentes, no implementado en todos los servicios.
- **Carga inicial de datos**: Los scripts pueden requerir ajustes según entorno.
- **Gestión de errores básica**: Falta robustez para producción.

---

## 🛠️ Justificación del diseño

### Neo4j (Editor Service)

- Modelo gráfico para representar relaciones entre áreas, salas, monstruos y tesoros.
- Consultas Cypher para caminos más cortos, entidades conectadas y cálculos acumulativos.

### Cassandra (Leaderboard Service)

- Optimizado para escritura rápida.
- Particionado por país.
- Agrupación por columnas para rankings ordenados automáticamente.
- Consistencia variable: `ONE` para eventos Horda, `LOCAL_QUORUM` para Hall of Fame.

### MongoDB (Wiki Service)

- Documentos anidados reflejan relaciones conceptuales.
- Eficiencia en consultas por ID y agregaciones estadísticas.
- Alta flexibilidad de esquema.

### Redis (Avatar Service)

- Índices HNSW para búsqueda vectorial con embeddings CLIP.
- Alta precisión y baja latencia para recomendaciones en tiempo real.