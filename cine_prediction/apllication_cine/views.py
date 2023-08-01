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
# def prediction_page(request):
#     # Récupérer le répertoire du fichier views.py (chemin relatif)
#     current_dir = os.path.dirname(os.path.abspath(__file__))
    
#     # Construire le chemin complet vers le fichier CSV en utilisant le chemin relatif
#     csv_path = os.path.normpath(os.path.join(current_dir, 'senscritique_scrapy/senscritique_scrapy/spiders/allocine_sortie.csv'))

#     # Charger les données du CSV en utilisant pandas
#     data = pd.read_csv(csv_path)

#     # Transmettre les données au template pour les afficher
#     return render(request, 'apllication_cine/prediction.html', context={'data': data})




def prediction_page(request):
    # Récupérer le répertoire du fichier views.py (chemin relatif)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construire le chemin complet vers le fichier CSV en utilisant le chemin relatif
    csv_path = os.path.normpath(os.path.join(current_dir, 'senscritique_scrapy/senscritique_scrapy/spiders/allocine_sortie.csv'))

    # Charger les données du CSV en utilisant pandas
    data = pd.read_csv(csv_path)

    # Charger le modèle pickles
    model_path = os.path.normpath(os.path.join(current_dir, 'test_cine.pkl'))
    with open(model_path, 'rb') as f:
        model = pickle.load(f)

    # Préparer les données pour la prédiction
    categorical_features = ["acteur_1", "acteur_2", "acteur_3", "réalisateur", "distributeur", "genre", "pays"]
    numerical_features = ["duree", "nominations", "prix", "annee_production"]
    X = data[categorical_features + numerical_features]

    # Faire la prédiction
    predictions = model.predict(X)

    # Ajouter les prédictions aux données
    data['prediction'] = np.floor(predictions / 2000).astype(int)
    data = data.sort_values(by='prediction', ascending=False)


    # Transmettre les données au template pour les afficher
    return render(request, 'apllication_cine/prediction.html', context={'data': data})










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
    # Récupérer les prédictions pour les films
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.normpath(os.path.join(current_dir, 'senscritique_scrapy/senscritique_scrapy/spiders/allocine_sortie.csv'))
    data = pd.read_csv(csv_path)
    model_path = os.path.normpath(os.path.join(current_dir, 'test_cine.pkl'))
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    categorical_features = ["acteur_1", "acteur_2", "acteur_3", "réalisateur", "distributeur", "genre", "pays"]
    numerical_features = ["duree", "nominations", "prix", "annee_production"]
    X = data[categorical_features + numerical_features]
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

def prediction_vs_reel_page(request):
    # Récupérer le répertoire du fichier views.py (chemin relatif)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Construire le chemin complet vers le fichier CSV en utilisant le chemin relatif
    csv_path = os.path.normpath(os.path.join(current_dir, 'senscritique_scrapy/senscritique_scrapy/spiders/allocine_sortie.csv'))
    # Charger les données du CSV en utilisant pandas
    data = pd.read_csv(csv_path)

    # Charger le modèle pickles
    model_path = os.path.normpath(os.path.join(current_dir, 'test_cine.pkl'))
    with open(model_path, 'rb') as f:
        model = pickle.load(f)

    # Préparer les données pour la prédiction
    categorical_features = ["acteur_1", "acteur_2", "acteur_3", "réalisateur", "distributeur", "genre", "pays"]
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
        
        # Enregistrer les données dans un nouveau fichier CSV
        data.to_csv(os.path.normpath(os.path.join(current_dir, 'prediction_VS_reel.csv')), index=False)

    # Trier les données par ordre décroissant en fonction de la colonne "prediction"
    data = data.sort_values(by='prediction', ascending=False)
        
    # Transmettre les données au template pour les afficher
    return render(request, 'apllication_cine/prediction_VS_reel.html', context={'data': data})