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
from django.db import transaction  # Importez le module transaction
import requests
import json



@register.filter
def mul(value, arg):
    return value * arg

@register.filter
def div(value, arg):
    return value / arg


# Create your views here.


def index(request):
    return render(request, 
                  'apllication_cine/index.html',
                 )


from django.shortcuts import render

def handler404(request, exception):
    return render(request, 'apllication_cine/404.html', status=404)

@login_required(login_url='login')  
def video(request):
    return render(request, 
                  'apllication_cine/video.html',
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
                return redirect('prediction')
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
            return redirect('prediction')
    return render(request, 'apllication_cine/signup.html', context={'form': form})


def delete_data(request):
    load_dotenv()

    server = os.environ['DB_SERVER']
    database = os.environ['DB_DATABASE']
    username = os.environ['DB_USERNAME']
    password = os.environ['DB_PASSWORD']
    driver = os.environ['DRIVER']

    cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)

    cursor = cnxn.cursor()
    cursor.execute("DELETE FROM [dbo].[films_prediction]")
    cnxn.commit()
    cursor.close()
    
    return HttpResponseRedirect(reverse('prediction'))


@login_required(login_url='login')
def prediction_page(request):
    load_dotenv()

    server = os.environ['DB_SERVER']
    database = os.environ['DB_DATABASE']
    username = os.environ['DB_USERNAME']
    password = os.environ['DB_PASSWORD']
    driver = os.environ['DRIVER']

    cnxn = pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)

    data = pd.read_sql_query('SELECT * FROM [dbo].[films_prediction]', cnxn)

    current_dir = os.path.dirname(os.path.abspath(__file__))

    categorical_features = ['vacances','saison','pays','annee_production','type','genre','genre1','langue']

    numeric_features = ['actor_1_popularity', 'actor_2_popularity',
        'actor_3_popularity','duree', 'director_popularity',  'nombre_films_distributeur', 'budget','reputation_distributeur']
    X = data[categorical_features + numeric_features]
    
    # print(X)

    is_data_empty = True

    if not data.empty:
        is_data_empty = False

        # Convertir les données du champ 'vacances' en booléen
        data['vacances'] = data['vacances'].astype(bool)

        input_data = []
        for index, row in X.iterrows():
            input_data.append({
                "duree": row['duree'],
                "genre": row['genre'],
                "pays": row['pays'],
                "type": row['type'],
                "annee_production": row['annee_production'],
                "actor_1_popularity": row['actor_1_popularity'],
                "actor_2_popularity": row['actor_2_popularity'],
                "actor_3_popularity": row['actor_3_popularity'],
                "director_popularity": row['director_popularity'],
                "vacances": row['vacances'],  # Les données ont été converties en booléen
                "saison": row['saison'],
                "langue": row['langue'],
                "budget": row['budget'],
                "genre1": row['genre1'],
                "reputation_distributeur": row['reputation_distributeur'],
                "nombre_films_distributeur": row['nombre_films_distributeur']
            })

        # Imprimer les données d'entrée envoyées à l'API
        # print("Input data sent to API:")
        # print(input_data)
        
        

        api_url = "http://fastapimodel.f0bae8f6bpfbazhu.francecentral.azurecontainer.io/predict/"
        response_data = []
        for elt in input_data:
            response = requests.post(api_url, json = elt)
            
            
            #print(response.status_code)
            
            
            #if response.status_code == 200:
            response_data.append( response.json() ) # Store the response data

        # Imprimer la réponse de l'API
        # print("Response from API:")
        # print(response.json())

        predictions = response_data
        # print("aaaaaaaaaaaaaaaa",predictions)

        data_loc = pd.DataFrame(predictions)
        data["prediction"] = data_loc['prediction'].apply(lambda x: round(x / 2000)).astype(int)
        data['prediction_national'] = data_loc['prediction']
        data['date'] = pd.to_datetime(data['date'], format='%d-%m-%Y')
        data = data.sort_values(by=['date', 'prediction'], ascending=[False, False])
        data['date'] = data['date'].dt.strftime('%d-%m-%Y')

    return render(request, 'apllication_cine/prediction.html', context={'data': data, 'is_data_empty': is_data_empty})




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


    

    
@login_required(login_url='login')   
def bot(request):
    load_dotenv()

    server = os.environ['DB_SERVER']
    database = os.environ['DB_DATABASE']
    username = os.environ['DB_USERNAME']
    password = os.environ['DB_PASSWORD']
    driver = os.environ['DRIVER']

    cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)

    data = pd.read_sql_query('SELECT * FROM [dbo].[films_prediction]', cnxn)

    if data.empty:
        return render(request, 'apllication_cine/bot.html', context={'is_data_empty': True})

    current_dir = os.path.dirname(os.path.abspath(__file__))

    categorical_features = ["acteur_1", "acteur_2", "acteur_3", "realisateur", "distributeur", "genre", "genre1" ,"pays", "langue",'vacances', 'saison', 'type','reputation_distributeur', 'nombre_films_distributeur']
    numerical_features = ["duree", "nominations", "prix", "annee_production", 'actor_1_popularity', 'actor_2_popularity', 'actor_3_popularity', 'director_popularity', 'budget']
    X = data[categorical_features + numerical_features]

    # Convertir les données en un format compatible avec l'API
    input_data = []
    for index, row in X.iterrows():
        input_data.append({
            "duree": row['duree'],
            "genre": row['genre'],
            "pays": row['pays'],
            "type": row['type'],
            "annee_production": row['annee_production'],
            "actor_1_popularity": row['actor_1_popularity'],
            "actor_2_popularity": row['actor_2_popularity'],
            "actor_3_popularity": row['actor_3_popularity'],
            "director_popularity": row['director_popularity'],
            "vacances": row['vacances'],  # Les données ont été converties en booléen
            "saison": row['saison'],
            "langue": row['langue'],
            "budget": row['budget'],
            "genre1": row['genre1'],
            "reputation_distributeur": row['reputation_distributeur'],
            "nombre_films_distributeur": row['nombre_films_distributeur']
        })

    # Envoyer les données à l'API et récupérer les prédictions
    api_url = "http://fastapimodel.f0bae8f6bpfbazhu.francecentral.azurecontainer.io/predict/"
    response_data = []
    for elt in input_data:
        response = requests.post(api_url, json=elt)
        response_data.append(response.json())  # Stocker les données de réponse

    predictions = response_data
    data_loc = pd.DataFrame(predictions)
    data["prediction"] = data_loc['prediction'].apply(lambda x: round(x / 2000)).astype(int)

    jours_semaine = ['mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche','lundi', 'mardi']
    jours_organises = {jour: [] for jour in jours_semaine}

    salle_capacities = [140, 100, 80, 80]

    data = data.sort_values(by='prediction', ascending=False)

    haute_prediction = data.nlargest(4, 'prediction')[['titre', 'prediction']].values.tolist()
    moyenne_prediction = data.nlargest(8, 'prediction', keep='last')[['titre', 'prediction']].nsmallest(4, 'prediction', keep='last')[['titre', 'prediction']].values.tolist()
    basse_prediction = data.nlargest(13, 'prediction')[['titre', 'prediction']].nsmallest(4, 'prediction', keep='last')[['titre', 'prediction']].values.tolist()

    jours_organises['mercredi'] = [[film[0], int(film[1] * 0.23)] for film in haute_prediction]
    jours_organises['samedi'] = [[film[0], int(film[1] * 0.38)] for film in haute_prediction]
    jours_organises['dimanche'] = [[film[0], int(film[1] * 0.38)] for film in haute_prediction]

    jours_organises['mardi'] = [[film[0], int(film[1] * 0.50)] for film in sorted(moyenne_prediction, key=lambda x: x[1], reverse=True)]
    jours_organises['vendredi'] = [[film[0], int(film[1] * 0.50)] for film in sorted(moyenne_prediction, key=lambda x: x[1], reverse=True)]

    jours_organises['lundi'] = [[film[0], int(film[1] * 0.50)] for film in sorted(basse_prediction, key=lambda x: x[1], reverse=True)]
    jours_organises['jeudi'] = [[film[0], int(film[1] * 0.50)] for film in sorted(basse_prediction, key=lambda x: x[1], reverse=True)]

    for jour, films in jours_organises.items():
        for film in films:
            prediction = film[1]
            salle_capacity = salle_capacities[films.index(film)]
            taux_remplissage = (prediction * 100) / salle_capacity
            film.append(taux_remplissage)

    return render(request, 'apllication_cine/bot.html', context={'jours_organises': jours_organises, 'salle_capacities': salle_capacities})


@register.filter
def get_item(list, index):
    return list[index]

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
# @login_required(login_url='login')

from datetime import datetime
from django.contrib import messages
@login_required(login_url='login')
def prediction_vs_reel_page(request):
    # Charger les variables d'environnement à partir du fichier .env
    load_dotenv()

    server = os.environ['DB_SERVER']
    database = os.environ['DB_DATABASE']
    username = os.environ['DB_USERNAME']
    password = os.environ['DB_PASSWORD']
    driver = os.environ['DRIVER']

    cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)

    data = pd.read_sql_query('SELECT * FROM [dbo].[films_prediction]', cnxn)

    if data.empty:
        return render(request, 'apllication_cine/bot.html', context={'is_data_empty': True})

    current_dir = os.path.dirname(os.path.abspath(__file__))

    categorical_features = ["acteur_1", "acteur_2", "acteur_3", "realisateur", "distributeur", "genre", "genre1" ,"pays", "langue",'vacances', 'saison', 'type','reputation_distributeur', 'nombre_films_distributeur']
    numerical_features = ["duree", "nominations", "prix", "annee_production", 'actor_1_popularity', 'actor_2_popularity', 'actor_3_popularity', 'director_popularity', 'budget']
    X = data[categorical_features + numerical_features]

    # Convertir les données en un format compatible avec l'API
    input_data = []
    for index, row in X.iterrows():
        input_data.append({
            "duree": row['duree'],
            "genre": row['genre'],
            "pays": row['pays'],
            "type": row['type'],
            "annee_production": row['annee_production'],
            "actor_1_popularity": row['actor_1_popularity'],
            "actor_2_popularity": row['actor_2_popularity'],
            "actor_3_popularity": row['actor_3_popularity'],
            "director_popularity": row['director_popularity'],
            "vacances": row['vacances'],  # Les données ont été converties en booléen
            "saison": row['saison'],
            "langue": row['langue'],
            "budget": row['budget'],
            "genre1": row['genre1'],
            "reputation_distributeur": row['reputation_distributeur'],
            "nombre_films_distributeur": row['nombre_films_distributeur']
        })

    # Envoyer les données à l'API et récupérer les prédictions
    api_url = "http://fastapimodel.f0bae8f6bpfbazhu.francecentral.azurecontainer.io/predict/"
    response_data = []
    for elt in input_data:
        response = requests.post(api_url, json=elt)
        response_data.append(response.json())  # Stocker les données de réponse

    predictions = response_data
    data_loc = pd.DataFrame(predictions)
    data["prediction"] = data_loc['prediction'].apply(lambda x: round(x / 2000)).astype(int)
    
    if request.method == 'POST':
        # Récupérer les résultats réels saisis par l'utilisateur
        real_results = [int(request.POST.get(f"real_result_{index}")) for index in range(len(data))]

        # Ajouter les résultats réels aux données
        data['real_result'] = real_results

        # Calculer la différence entre les résultats réels et les prédictions
        data['difference'] = np.where(data['real_result'] == 0, "n'a pas été projeté", data['real_result'] - data['prediction'])

        # Enregistrer les données dans la base de données Azure
        cursor = cnxn.cursor()
        with transaction.atomic():
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
                    cursor.execute("DELETE FROM [dbo].[films_prediction] WHERE titre = ?", row["titre"])
            cnxn.commit()
        messages.success(request, 'Les informations ont bien été envoyées.')

    # Trier les données par ordre décroissant en fonction de la colonne "prediction"
    data = data.sort_values(by='prediction', ascending=False)
        
    # Transmettre les données au template pour les afficher
    return render(request, 'apllication_cine/prediction_VS_reel.html', context={'data': data})
