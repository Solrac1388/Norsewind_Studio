// Crear restricciones e índices
CREATE CONSTRAINT Area_name IF NOT EXISTS FOR (a:Area) REQUIRE a.name IS UNIQUE;
CREATE CONSTRAINT Room_id IF NOT EXISTS FOR (r:Room) REQUIRE r.room_id IS UNIQUE;
CREATE CONSTRAINT Monster_id IF NOT EXISTS FOR (m:Monster) REQUIRE m.id IS UNIQUE;
CREATE CONSTRAINT Loot_id IF NOT EXISTS FOR (l:Loot) REQUIRE l.id IS UNIQUE;

// Crear áreas
CREATE (a1:Area {name: "Jolly Steppe of Emerald city"});
CREATE (a2:Area {name: "Uptight Shrubland of Avalon"});
CREATE (a3:Area {name: "Insane Jungle of Gondor"});
CREATE (a4:Area {name: "Embarrassed Swamp of Fafnir"});
CREATE (a5:Area {name: "Empowered Steppe of Isengard"});
CREATE (a6:Area {name: "Terrible Moor of Babylon"});
CREATE (a7:Area {name: "Clumsy Tropical Rainforest of Bilbo"});
CREATE (a8:Area {name: "Terrible River of Gandalf"});
CREATE (a9:Area {name: "Panicky Desert of Fomalhaut"});
CREATE (a10:Area {name: "Old-Fashioned Mountain of Emerald city"});

// Conectar algunas áreas directamente
MATCH (a1:Area {name: "Jolly Steppe of Emerald city"}),
      (a2:Area {name: "Uptight Shrubland of Avalon"})
CREATE (a1)-[:IS_CONNECTED]->(a2);

MATCH (a2:Area {name: "Uptight Shrubland of Avalon"}),
      (a3:Area {name: "Insane Jungle of Gondor"})
CREATE (a2)-[:IS_CONNECTED]->(a3);

// Crear salas con conexiones a áreas
MATCH (a1:Area {name: "Jolly Steppe of Emerald city"})
CREATE (r1:Room {room_id: 1, room_name: "Entrada", dungeon_name: "Bentclock, Laboratory of the Sexy Thieves"}),
       (r2:Room {room_id: 2, room_name: "Sala Principal", dungeon_name: "Bentclock, Laboratory of the Sexy Thieves"}),
       (r3:Room {room_id: 3, room_name: "Salida", dungeon_name: "Bentclock, Laboratory of the Sexy Thieves"}),
       (r1)-[:IS_CONNECTED]->(r2),
       (r2)-[:IS_CONNECTED]->(r3),
       (a1)<-[:IS_CONNECTED]-(r1);

// Crear monstruos
CREATE (m1:Monster {id: 1, name: "Goblin", level: 1, exp: 50, type: "Humanoid"});
CREATE (m2:Monster {id: 2, name: "Beholder", level: 100, exp: 5000, type: "Aberration"});
CREATE (m3:Monster {id: 3, name: "Zombie", level: 1, exp: 25, type: "Undead"});

// Crear tesoros
CREATE (l1:Loot {id: 1, name: "Gold Coin", type1: "Currency", gold: 1});
CREATE (l2:Loot {id: 2, name: "Magic Sword", type1: "Weapon", type2: "Magic", gold: 500});
CREATE (l3:Loot {id: 3, name: "Health Potion", type1: "Consumable", gold: 50});

// Asignar monstruos y tesoros a salas
MATCH (r1:Room {room_id: 1}), (m1:Monster {id: 1})
CREATE (r1)-[:CONTAINS {amount: 2}]->(m1);

MATCH (r2:Room {room_id: 2}), (m2:Monster {id: 2})
CREATE (r2)-[:CONTAINS {amount: 1}]->(m2);

MATCH (r3:Room {room_id: 3}), (l1:Loot {id: 1})
CREATE (r3)-[:CONTAINS {amount: 100}]->(l1);

MATCH (r2:Room {room_id: 2}), (l2:Loot {id: 2})
CREATE (r2)-[:CONTAINS {amount: 1}]->(l2);

// Crear mazmorra conectando áreas
MATCH (a2:Area {name: "Uptight Shrubland of Avalon"})
CREATE (r4:Room {room_id: 4, room_name: "Entrada", dungeon_name: "Arvalecliffe, Laboratory of the Unsightly Ninjas"}),
       (r5:Room {room_id: 5, room_name: "Sala Principal", dungeon_name: "Arvalecliffe, Laboratory of the Unsightly Ninjas"}),
       (r6:Room {room_id: 6, room_name: "Salida", dungeon_name: "Arvalecliffe, Laboratory of the Unsightly Ninjas"}),
       (r4)-[:IS_CONNECTED]->(r5),
       (r5)-[:IS_CONNECTED]->(r6),
       (a2)<-[:IS_CONNECTED]-(r4);

MATCH (a3:Area {name: "Insane Jungle of Gondor"}),
      (r6:Room {room_id: 6})
CREATE (a3)<-[:IS_CONNECTED]-(r6);