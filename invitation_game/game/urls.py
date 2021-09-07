from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # path('invitation/', views.invitation, name='invitation-form'),
    # path('<int:game>/', views.game, name='game-form'),
    # path('<int:game>/questions', views.update_questions, name='question-form'),
    # path('<int:game>/character', views.update_character, name='character-form'),
    # path('<name>', views.home, name='home-name'),
    path('json/<int:id>/', views.json_show, name='json-id'),
    path('json/<int:id>/scores/', views.json_scores, name='json-scores'),
    path('json/<str:wedding_url>/', views.json_user, name='json-user')

]