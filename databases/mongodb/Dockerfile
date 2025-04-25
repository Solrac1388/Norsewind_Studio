FROM mongo:latest

# Copiamos los scripts de inicialización
COPY ./assets/collections/init-mongo.js /docker-entrypoint-initdb.d/
COPY ./assets/collections/import-data.sh /docker-entrypoint-initdb.d/

# Nos aseguramos de que el script de importación sea ejecutable
RUN chmod +x /docker-entrypoint-initdb.d/import-data.sh

# Creamos el directorio de datos si no existe
RUN mkdir -p /docker-entrypoint-initdb.d/data

# Variable de entorno
ENV MONGO_INITDB_DATABASE=jotun_wiki

# Puerto para MongoDB
EXPOSE 27017
