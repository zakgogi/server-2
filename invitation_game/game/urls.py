from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('<name>', views.home, name='home-name'),
    path('json/<int:id>/', views.json_show, name='json-id'),
    path('json/<int:id>/scores/', views.json_scores, name='json-scores')

]