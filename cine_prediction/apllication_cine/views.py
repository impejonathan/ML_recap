# authentication/views.py
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate , logout
from django.http import HttpResponseRedirect
from django.urls import reverse

from . import forms
from django.contrib.auth.decorators import login_required
import pandas as pd
import os
from joblib import load
import pickle
import numpy as np
import subprocess

from django.template.defaulttags import register
import pyodbc
from dotenv import load_dotenv


# Create your views here.


def index(request):
    return render(request, 
                  'apllication_cine/index.html',
                  )
    
def logout_user(request):
    
    logout(request)
    return redirect('login')



def login_page(request):
    form = forms.LoginForm()
    message = ''
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('home')
        message = 'Identifiants invalides.'
    return render(request, 'apllication_cine/login.html', context={'form': form, 'message': message})


def signup_page(request):
    form = forms.SignupForm()
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # auto-login user
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, 'apllication_cine/signup.html', context={'form': form})





# # @login_required(login_url='login')

def prediction_page(request):
    # Charger les variables d'environnement à partir du fichier .env
    load_dotenv()

    # Récupérer les informations de connexion à la base de données à partir des variables d'environnement
    server = os.environ['DB_SERVER']
    database = os.environ['DB_DATABASE']
    username = os.environ['DB_USERNAME']
    password = os.environ['DB_PASSWORD']
    driver = os.environ['DRIVER']

    # Construire la chaîne de connexion à la base de données
    cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)

    # Exécuter une requête SQL pour récupérer les données de la table films_prediction
    data = pd.read_sql_query('SELECT * FROM [dbo].[films_prediction]', cnxn)

    # Récupérer le répertoire du fichier views.py (chemin relatif)
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Charger le modèle pickles
    model_path = os.path.normpath(os.path.join(current_dir, 'test_model_jo.pkl'))
    with open(model_path, 'rb') as f:
        model = pickle.load(f)

    # Préparer les données pour la prédiction
    categorical_features = ["acteur_1", "acteur_2", "acteur_3", "realisateur", "distributeur", "genre", "pays"]
    numerical_features = ["duree", "nominations", "prix", "annee_production"]
    X = data[categorical_features + numerical_features]

    # Faire la prédiction
    predictions = model.predict(X)

    # Ajouter les prédictions aux données
    data['prediction'] = np.floor(predictions / 2000).astype(int)
    data = data.sort_values(by='prediction', ascending=False)

    # Transmettre les données au template pour les afficher
    return render(request, 'apllication_cine/prediction.html', context={'data': data})



# def prediction_page(request):
#     # Récupérer le répertoire du fichier views.py (chemin relatif)
#     current_dir = os.path.dirname(os.path.abspath(__file__))
    
#     # Construire le chemin complet vers le fichier CSV en utilisant le chemin relatif
#     csv_path = os.path.normpath(os.path.join(current_dir, 'senscritique_scrapy/senscritique_scrapy/spiders/allocine_sortie.csv'))

#     # Charger les données du CSV en utilisant pandas
#     data = pd.read_csv(csv_path)

#     # Charger le modèle pickles
#     model_path = os.path.normpath(os.path.join(current_dir, 'test_cine.pkl'))
#     with open(model_path, 'rb') as f:
#         model = pickle.load(f)

#     # Préparer les données pour la prédiction
#     categorical_features = ["acteur_1", "acteur_2", "acteur_3", "réalisateur", "distributeur", "genre", "pays"]
#     numerical_features = ["duree", "nominations", "prix", "annee_production"]
#     X = data[categorical_features + numerical_features]

#     # Faire la prédiction
#     predictions = model.predict(X)

#     # Ajouter les prédictions aux données
#     data['prediction'] = np.floor(predictions / 2000).astype(int)
#     data = data.sort_values(by='prediction', ascending=False)


#     # Transmettre les données au template pour les afficher
#     return render(request, 'apllication_cine/prediction.html', context={'data': data})







def scraping_view(request):
    if request.method == 'POST':
        # Récupérer le répertoire du fichier views.py (chemin relatif)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Construire le chemin complet vers le répertoire du spider en utilisant le chemin relatif
        spider_dir = os.path.normpath(os.path.join(current_dir, 'senscritique_scrapy/senscritique_scrapy/spiders'))
        # Exécuter le spider
        subprocess.run(["scrapy", "crawl", "allocine_sortie", "-O", "allocine_sortie.csv"], cwd=spider_dir)
        # Rediriger l'utilisateur vers la page de prédiction
        return HttpResponseRedirect(reverse('prediction'))

    
    
    
    
    
    
    
    
    
    
 
    
    
    
    
# @login_required(login_url='login')   
def bot(request):
    # Charger les variables d'environnement à partir du fichier .env
    load_dotenv()

    # Récupérer les informations de connexion à la base de données à partir des variables d'environnement
    server = os.environ['DB_SERVER']
    database = os.environ['DB_DATABASE']
    username = os.environ['DB_USERNAME']
    password = os.environ['DB_PASSWORD']
    driver = os.environ['DRIVER']

    # Construire la chaîne de connexion à la base de données
    cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)

    # Exécuter une requête SQL pour récupérer les données de la table films_prediction
    data = pd.read_sql_query('SELECT * FROM [dbo].[films_prediction]', cnxn)

    # Récupérer le répertoire du fichier views.py (chemin relatif)
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Charger le modèle pickles
    model_path = os.path.normpath(os.path.join(current_dir, 'test_model_jo.pkl'))
    with open(model_path, 'rb') as f:
        model = pickle.load(f)

    # Préparer les données pour la prédiction
    categorical_features = ["acteur_1", "acteur_2", "acteur_3", "realisateur", "distributeur", "genre", "pays"]
    numerical_features = ["duree", "nominations", "prix", "annee_production"]
    X = data[categorical_features + numerical_features]

    # Faire la prédiction
    predictions = model.predict(X)
    data['prediction'] = np.floor(predictions / 2000).astype(int)

    # Organiser les films en fonction des jours de la semaine
    jours_semaine = [ 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche','lundi', 'mardi']
    jours_organises = {jour: [] for jour in jours_semaine}

    # Charger les capacités des salles de cinéma
    salle_capacities = [140, 100, 80, 80]

    # Trier les films par prédiction (du plus élevé au plus faible)
    data = data.sort_values(by='prediction', ascending=False)

    # Séparer les films en trois listes : haute, moyenne et basse prédiction
    haute_prediction = data.nlargest(4, 'prediction')[['titre', 'prediction']].values.tolist()
    moyenne_prediction = data.nlargest(8, 'prediction', keep='last')[['titre', 'prediction']].nsmallest(4, 'prediction', keep='last')[['titre', 'prediction']].values.tolist()
    basse_prediction = data.nlargest(13, 'prediction')[['titre', 'prediction']].nsmallest(4, 'prediction', keep='last')[['titre', 'prediction']].values.tolist()

    # Organiser les films en fonction des jours de la semaine
    jours_organises['mercredi'] = [[film[0], int(film[1] * 0.23)] for film in haute_prediction]
    jours_organises['samedi'] = [[film[0], int(film[1] * 0.38)] for film in haute_prediction]
    jours_organises['dimanche'] = [[film[0], int(film[1] * 0.38)] for film in haute_prediction]

    jours_organises['mardi'] = [[film[0], int(film[1] * 0.50)] for film in sorted(moyenne_prediction, key=lambda x: x[1], reverse=True)]
    jours_organises['vendredi'] = [[film[0], int(film[1] * 0.50)] for film in sorted(moyenne_prediction, key=lambda x: x[1], reverse=True)]

    jours_organises['lundi'] = [[film[0], int(film[1] * 0.50)] for film in sorted(basse_prediction, key=lambda x: x[1], reverse=True)]
    jours_organises['jeudi'] = [[film[0], int(film[1] * 0.50)] for film in sorted(basse_prediction, key=lambda x: x[1], reverse=True)]
    
    return render(request, 'apllication_cine/bot.html', context={'jours_organises': jours_organises, 'salle_capacities': salle_capacities})

    
@register.filter
def get_item(list, index):
        return list[index]


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
# @login_required(login_url='login')

from datetime import datetime
from django.contrib import messages

def prediction_vs_reel_page(request):
    # Charger les variables d'environnement à partir du fichier .env
    load_dotenv()

    # Récupérer les informations de connexion à la base de données à partir des variables d'environnement
    server = os.environ['DB_SERVER']
    database = os.environ['DB_DATABASE']
    username = os.environ['DB_USERNAME']
    password = os.environ['DB_PASSWORD']
    driver = os.environ['DRIVER']

    # Construire la chaîne de connexion à la base de données
    cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)

    # Exécuter une requête SQL pour récupérer les données de la table films_prediction
    data = pd.read_sql_query('SELECT * FROM [dbo].[films_prediction]', cnxn)

    # Récupérer le répertoire du fichier views.py (chemin relatif)
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Charger le modèle pickles
    model_path = os.path.normpath(os.path.join(current_dir, 'test_model_jo.pkl'))
    with open(model_path, 'rb') as f:
        model = pickle.load(f)

    # Préparer les données pour la prédiction
    categorical_features = ["acteur_1", "acteur_2", "acteur_3", "realisateur", "distributeur", "genre", "pays"]
    numerical_features = ["duree", "nominations", "prix", "annee_production"]
    X = data[categorical_features + numerical_features]

    # Faire la prédiction
    predictions = model.predict(X)

    # Ajouter les prédictions aux données
    data['prediction'] = np.floor(predictions / 2000).astype(int)
    
    if request.method == 'POST':
        # Récupérer les résultats réels saisis par l'utilisateur
        real_results = [int(request.POST.get(f"real_result_{index}")) for index in range(len(data))]
        
        # Ajouter les résultats réels aux données
        data['real_result'] = real_results
        
        # Calculer la différence entre les résultats réels et les prédictions
        data['difference'] = np.where(data['real_result'] == 0, "n'a pas été projeté", data['real_result'] - data['prediction'])
        
        # Enregistrer les données dans la base de données Azure
        cursor = cnxn.cursor()
        for index, row in data.iterrows():
            if row["real_result"] != 0:
                cursor.execute("""
                    MERGE INTO [dbo].[films] AS target
                    USING (VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?))
                    AS source (titre, acteur_1, acteur_2, acteur_3, realisateur, distributeur, duree, genre, pays, nominations, prix, annee_production, Entrees_1ere_semaine)
                    ON target.titre = source.titre
                    WHEN MATCHED THEN UPDATE SET 
                        target.acteur_1 = source.acteur_1,
                        target.acteur_2 = source.acteur_2,
                        target.acteur_3 = source.acteur_3,
                        target.realisateur = source.realisateur,
                        target.distributeur = source.distributeur,
                        target.duree = source.duree,
                        target.genre = source.genre,
                        target.pays = source.pays,
                        target.nominations = source.nominations,
                        target.prix = source.prix,
                        target.annee_production = source.annee_production,
                        target.Entrees_1ere_semaine = source.Entrees_1ere_semaine,
                        target.sortie_france = ?
                    WHEN NOT MATCHED THEN INSERT (titre, acteur_1, acteur_2, acteur_3, realisateur, distributeur, duree, genre, pays, nominations, prix, annee_production, Entrees_1ere_semaine, sortie_france)
                    VALUES (source.titre, source.acteur_1, source.acteur_2, source.acteur_3, source.realisateur, source.distributeur, source.duree, source.genre, source.pays, source.nominations, source.prix, source.annee_production, source.Entrees_1ere_semaine, ?);
                """, row["titre"], row["acteur_1"], row["acteur_2"], row["acteur_3"], row["realisateur"], row["distributeur"], row["duree"], row["genre"], row["pays"], row["nominations"], row["prix"], row["annee_production"], row["real_result"] * 2000, datetime.now().strftime('%Y-%m-%d'), datetime.now().strftime('%Y-%m-%d'))
        cnxn.commit()
        messages.success(request, 'Les informations ont bien été envoyées.')

    # Trier les données par ordre décroissant en fonction de la colonne "prediction"
    data = data.sort_values(by='prediction', ascending=False)
        
    # Transmettre les données au template pour les afficher
    return render(request, 'apllication_cine/prediction_VS_reel.html', context={'data': data})
