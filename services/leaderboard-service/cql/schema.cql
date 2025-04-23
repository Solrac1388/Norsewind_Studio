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
  completed_count int,
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