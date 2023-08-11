# Importation des modules nécessaires
import os
import joblib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Définition de la classe BaseModel pour les données d'entrée de prédiction
from pydantic import BaseModel

# Création d'une instance FastAPI
app = FastAPI()

class InputData(BaseModel):
    duree: float
    genre: str
    pays: str
    type: str
    annee_production: int
    actor_1_popularity: float
    actor_2_popularity: float
    actor_3_popularity: float
    director_popularity: float
    vacances: bool
    saison: str
    langue: str
    budget: float
    genre1: str
    reputation_distributeur: float
    nombre_films_distributeur: int


# class PredictionOut(BaseModel):
#     Entrees_1ere_semaine: int

class PredictionOut(BaseModel):
    prediction: int


    


# Construction du chemin absolu vers le modèle
model_path = os.path.join(os.path.dirname(__file__), '../../model/catboost.pkl')

# Chargement du modèle depuis le fichier
model = joblib.load(model_path)

# Définition de l'endpoint /predict/
from pandas import DataFrame 
import pandas as pd


@app.post('/predict/', response_model=PredictionOut)
async def predict(input_data: InputData):
    # Créer un DataFrame pandas à partir des données d'entrée
    input_df = pd.DataFrame([{
        'vacances': input_data.vacances,
        'saison': input_data.saison,
        'pays': input_data.pays,
        'annee_production': input_data.annee_production,
        'type': input_data.type,
        'genre': input_data.genre,
        'genre1': input_data.genre1,
        'langue': input_data.langue,
        'actor_1_popularity': input_data.actor_1_popularity,
        'actor_2_popularity': input_data.actor_2_popularity,
        'actor_3_popularity': input_data.actor_3_popularity,
        'duree': input_data.duree,
        'director_popularity': input_data.director_popularity,
        'nombre_films_distributeur': input_data.nombre_films_distributeur,
        'budget': input_data.budget,
        'reputation_distributeur': input_data.reputation_distributeur
    }])
    
   
    # Faire la prédiction avec le modèle
    #int(best_model.predict(X.head(1))[0]) : il sort un entier
    
    Entrees_1ere_semaine = model.predict(input_df)
    
    # Convertir l'objet numpy array en entier Python
    prediction_int = int(Entrees_1ere_semaine[0])

    # Retourner la prédiction
    return {"prediction": prediction_int}



