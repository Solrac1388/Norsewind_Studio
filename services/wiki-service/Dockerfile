FROM node:18-alpine

WORKDIR /app

# Copiamos los archivos de configuración del proyecto
COPY package*.json ./

# Instalamos dependencias
RUN npm install

# Copiamos el código fuente
COPY . .

# Exponemos el puerto de la aplicación
EXPOSE 8080

# Iniciamos la aplicación
CMD ["npm", "start"]
