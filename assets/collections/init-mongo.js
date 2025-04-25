db = db.getSiblingDB('jotun_wiki');

// Esquemas para las colecciones
const roomSchema = {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["room_id", "room_name", "dungeon_id", "dungeon_name"],
      properties: {
        room_id: { bsonType: "int" },
        room_name: { bsonType: "string" },
        dungeon_id: { bsonType: "int" },
        dungeon_name: { bsonType: "string" },
        in_waypoint: { bsonType: ["string", "null"] },
        out_waypoint: { bsonType: ["string", "null"] },
        rooms_connected: { bsonType: "array" },
        hints: { bsonType: "array" },
        monsters: { bsonType: "array" },
        loot: { bsonType: "array" }
      }
    }
  }
};

const userSchema = {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["email", "user_name", "creation_date"],
      properties: {
        email: { bsonType: "string" },
        user_name: { bsonType: "string" },
        creation_date: { bsonType: "string" },
        country: { bsonType: ["string", "null"] },
        hints: { bsonType: "array" }
      }
    }
  }
};

const lootSchema = {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["id", "name"],
      properties: {
        id: { bsonType: "int" },
        name: { bsonType: "string" },
        type1: { bsonType: ["string", "null"] },
        type2: { bsonType: ["string", "null"] },
        weight: { bsonType: ["string", "null"] },
        gold: { bsonType: ["int", "null"] }
      }
    }
  }
};

const monsterSchema = {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["id", "name"],
      properties: {
        id: { bsonType: "int" },
        name: { bsonType: "string" },
        place: { bsonType: ["string", "null"] },
        type: { bsonType: ["string", "null"] },
        man_page: { bsonType: ["string", "null"] },
        level: { bsonType: ["int", "null"] },
        exp: { bsonType: ["int", "null"] }
      }
    }
  }
};

// Creamos las colecciones con validación de esquema
db.createCollection("rooms", roomSchema);
db.createCollection("users", userSchema);
db.createCollection("loot", lootSchema);
db.createCollection("monsters", monsterSchema);

// Creamos índices para mejorar el rendimiento
db.rooms.createIndex({ "room_id": 1 }, { unique: true });
db.users.createIndex({ "email": 1 }, { unique: true });
db.loot.createIndex({ "id": 1 }, { unique: true });
db.monsters.createIndex({ "id": 1 }, { unique: true });
