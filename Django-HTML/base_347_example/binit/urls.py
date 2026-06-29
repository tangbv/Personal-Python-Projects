# binit/urls.py
from django.urls import path

from . import views
app_name = 'binit' # Namespace for the app

urlpatterns = [
  path('', views.index, name='index'),
  path('start/', views.start_game, name='start_game'),
  path('play/', views.play_game, name='play_game'),
  path('results/', views.game_result, name='game_results'),
]
