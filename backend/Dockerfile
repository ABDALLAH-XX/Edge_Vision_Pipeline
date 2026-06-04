# Utiliser une image Python officielle légère
FROM python:3.10-slim

# Éviter que Python écrive des fichiers .pyc et forcer l'affichage des logs en temps réel
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Installer les dépendances système requises pour OpenCV (version mise à jour)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Définir le dossier de travail
WORKDIR /app

# Copier et installer les dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code du backend (y compris le dossier du modèle)
COPY . .

# Exposer le port de FastAPI
EXPOSE 8000

# Commande pour lancer le serveur
CMD ["python", "main.py"]