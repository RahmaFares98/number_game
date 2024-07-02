# Great Number Game_assig/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('winner', views.winner),
    path('playagain', views.playagain),
    path('loser', views.loser),
    path('leaderboard', views.leaderboard),

    
]