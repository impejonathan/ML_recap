# FastAPI 

Cet API prend en charge les requêtes POST avec des données d'entrée JSON et renvoie les prédictions.

## Configuration Requise

    Python 3.x
    Bibliothèques Python : FastAPI, joblib, pandas, uvicorn

## Utilisation

    Placez votre modèle CatBoost pré-entraîné au format pickle dans le répertoire model.

    Modifiez le fichier main.py pour refléter les caractéristiques de votre modèle et les données d'entrée.

    Exécutez l'application FastAPI :

    sh:

    python run.py

    Accédez à l'API à l'adresse http://localhost:8000.

## Endpoint API

    POST /predict/ : Effectue une prédiction d'entrées en première semaine pour un film en fonction des caractéristiques fournies. Les données d'entrée doivent être au format JSON.