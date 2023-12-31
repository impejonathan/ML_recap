"""cine_prediction URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from apllication_cine import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', views.index ),
    path('', views.login_page, name='login'),
    path('signup', views.signup_page, name='signup'),
    path('logout/', views.logout_user, name='logout'),
    path('prediction', views.prediction_page, name='prediction'),
    path('bot', views.bot, name='bot'),
    path('prediction_VS_reel', views.prediction_vs_reel_page, name='prediction_VS_reel'),
    path('scraping/', views.scraping_view, name='scraping'),
    path('delete_data/', views.delete_data, name='delete_data'),
    path('video/', views.video, name='video' ),
    
    # path('historique/', views.historique_view, name='historique'),
]

handler404 = 'apllication_cine.views.handler404'
