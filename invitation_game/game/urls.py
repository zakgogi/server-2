from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('invitation/', views.invitation, name='invitation-form'),
    path('<int:gamenumber>/', views.game, name='game-form'),
    path('<int:gamenumber>/questions/<str:name>', views.update_questions, name='question-form'),
    path('<int:gamenumber>/character', views.update_character, name='character-form'),
    path('json/<int:id>/', views.json_show, name='json-id'),
    path('json/<int:id>/scores/', views.json_scores, name='json-scores'),
    path('json/<str:wedding_url>/', views.json_user, name='json-user')

]