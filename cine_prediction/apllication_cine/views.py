# authentication/views.py
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate , logout
from . import forms
from django.contrib.auth.decorators import login_required
import pandas as pd
import os

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





# @login_required(login_url='login')
def prediction_page(request):
    # Récupérer le répertoire du fichier views.py (chemin relatif)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construire le chemin complet vers le fichier CSV en utilisant le chemin relatif
    csv_path = os.path.normpath(os.path.join(current_dir, 'senscritique_scrapy/senscritique_scrapy/spiders/allocine_sortie.csv'))

    # Charger les données du CSV en utilisant pandas
    data = pd.read_csv(csv_path)

    # Transmettre les données au template pour les afficher
    return render(request, 'apllication_cine/prediction.html', context={'data': data})

    
# @login_required(login_url='login')   
def envoi_prediction_page(request):
    return render(request, 
                  'apllication_cine/envoi_prediction.html',
                  )
    
    
    
# @login_required(login_url='login')
def prediction_VS_reel_page(request):
    return render(request, 
                  'apllication_cine/prediction_VS_reel.html',
                  )
    