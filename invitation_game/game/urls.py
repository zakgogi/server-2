from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('<name>', views.home, name='home-name')
]