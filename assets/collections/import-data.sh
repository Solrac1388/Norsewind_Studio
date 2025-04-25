#!/bin/bash
# Espera a que MongoDB esté listo
sleep 5
# Importa los datos (nota: usa "loots" en lugar de "loot" para coincidir con la colección creada)
mongoimport --host localhost --db jotun_wiki --collection monsters --file /docker-entrypoint-initdb.d/data/monsters.json --jsonArray
mongoimport --host localhost --db jotun_wiki --collection loots --file /docker-entrypoint-initdb.d/data/loot.json --jsonArray
mongoimport --host localhost --db jotun_wiki --collection users --file /docker-entrypoint-initdb.d/data/users.json --jsonArray
mongoimport --host localhost --db jotun_wiki --collection rooms --file /docker-entrypoint-initdb.d/data/rooms.json --jsonArray
echo "Datos importados correctamente"
