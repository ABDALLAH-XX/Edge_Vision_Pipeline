# Utiliser l'image Node officielle
FROM node:20-slim

WORKDIR /app

# Copier les fichiers de configuration des dépendances
COPY package*.json ./

# Installer les dépendances
RUN npm install

# Copier le reste du code du frontend
COPY . .

# Exposer le port par défaut de Vite
EXPOSE 5173

# Lancer Vite en mode "host" pour qu'il soit accessible depuis l'extérieur du conteneur
CMD ["npm", "run", "dev", "--", "--host"]