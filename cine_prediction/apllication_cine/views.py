# authentication/views.py
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate , logout
from . import forms
from django.contrib.auth.decorators import login_required

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
    return render(request, 
                  'apllication_cine/prediction.html',
                  )
    
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
    