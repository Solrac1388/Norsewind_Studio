-- Consultas de lectura
-- Hall of Fame (LOCAL_QUORUM)
CONSISTENCY LOCAL_QUORUM;
SELECT email, user_name, minutes, date FROM hall_of_fame 
WHERE country = ? AND dungeon_id = ? AND year = ? AND month = ? 
LIMIT 5;

-- Estadísticas de jugador (LOCAL_QUORUM)
CONSISTENCY LOCAL_QUORUM;
SELECT dungeon_id, avg_minutes FROM player_stats 
WHERE email = ? AND year = ?;

-- Ranking de Horda (ONE)
CONSISTENCY ONE;
SELECT user_id, user_name, email, n_killed FROM horde_ranking 
WHERE event_id = ? AND country = ? 
LIMIT 50;

-- Consultas de escritura
-- Registrar completación de mazmorra (LOCAL_QUORUM para consistencia)
CONSISTENCY LOCAL_QUORUM;
INSERT INTO hall_of_fame (country, dungeon_id, year, month, email, user_name, minutes, date)
VALUES (?, ?, ?, ?, ?, ?, ?, ?);

-- Actualizar estadísticas de jugador (LOCAL_QUORUM)
CONSISTENCY LOCAL_QUORUM;
UPDATE player_stats 
SET avg_minutes = ?, completed_count = completed_count + 1
WHERE email = ? AND year = ? AND dungeon_id = ?;

-- Registrar eliminación de monstruo (ONE para velocidad)
CONSISTENCY ONE;
UPDATE horde_ranking 
SET n_killed = n_killed + 1
WHERE event_id = ? AND country = ? AND user_id = ?;