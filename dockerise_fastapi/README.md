# Dockerisation de l'API FastAPI

Ce readme vous guide à travers le processus de dockerisation d'une API FastAPI utilisant Docker. L'API prédit les entrées en première semaine pour les films en utilisant un modèle CatBoost pré-entraîné.
## Configuration Requise

    Docker
    Docker Compose (facultatif, mais recommandé)

## Utilisation

    Clonez ce dépôt :

    sh

    git clone <lien-du-dépôt>

Accédez au répertoire du projet :

sh

cd <nom-du-répertoire>

Placez votre modèle CatBoost pré-entraîné au format pickle dans le répertoire app/model.

Modifiez le fichier app/main.py pour refléter les caractéristiques de votre modèle et les données d'entrée.

Construisez l'image Docker :

sh

docker build -t fastapi-prediction .

Exécutez le conteneur Docker :

sh

docker run -d -p 8000:80 fastapi-prediction

Accédez à l'API à l'adresse http://localhost:8000.