# Usa la imagen oficial de Node.js versión 18 como base
FROM node:18

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo package.json para instalar las dependencias
COPY package.json .

# Instala las dependencias definidas en package.json
RUN npm install

# Copia todos los archivos del proyecto al contenedor
COPY . .

# Comando para iniciar la aplicación (según lo definido en package.json)
CMD ["npm", "start"]
