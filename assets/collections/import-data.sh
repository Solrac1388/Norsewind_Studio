#!/bin/bash
mongoimport --host mongodb --db jotun_wiki --collection monsters --file /docker-entrypoint-initdb.d/data/monsters.json --jsonArray
mongoimport --host mongodb --db jotun_wiki --collection loot --file /docker-entrypoint-initdb.d/data/loot.json --jsonArray
mongoimport --host mongodb --db jotun_wiki --collection users --file /docker-entrypoint-initdb.d/data/users.json --jsonArray
mongoimport --host mongodb --db jotun_wiki --collection rooms --file /docker-entrypoint-initdb.d/data/rooms.json --jsonArray
