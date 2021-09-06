from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import  JsonResponse
from django.views.decorators.csrf import csrf_exempt

import json

from .serializers import GameSerializer, GameScoresSerializer,  UserSerializer
from .models import Question, Character, Score, Invitation, Game, Profile
from .forms import NewGameForm

# Create your views here.

def home(req, name = 'person'):
        context = {"name": name}
    
        return render(req, "game/index.html", context)

@login_required
def create(request):
    if request.method == 'POST':
        game = NewGameForm(request.POST)
        if game.is_valid():
            game_id = game.save().id
            return redirect("game-show", id=game_id)
    else:
        form = NewGameForm()
    data = {'form': form, 'questions':''}
    return render(request, 'game/new.html', data)
        

@login_required
def show(request, id):
    article = get_object_or_404(Article, pk=id)
    if request.method == 'POST':
        form = DeleteArticleForm(request.POST)
        if form.is_valid():
            article.delete()
            return redirect("home")
    else:
        form = DeleteArticleForm()
    data = {
        'article': article,
        'form': form
    }
    return render(request, 'articles/management/show.html', data)

def not_found_404(request, exception):
    data = { 'err': exception }
    return render(request, 'game/404.html', data)

def server_error_500(request):
    return render(request, 'game/500.html')

''' REST APP '''
def json_show(request, id):
    game = get_object_or_404(Game, pk=id) 
    serializer = GameSerializer(game)
    return JsonResponse(serializer.data, safe=False)

@csrf_exempt
def json_scores(request, id):
    if request.method == 'GET':
        game = get_object_or_404(Game, pk=id) 
        serializer = GameScoresSerializer(game)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'PATCH':
        game = get_object_or_404(Game, pk=id) 
        serializer = GameScoresSerializer(game, data=json.loads(request.body))
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.data, safe=False) 

def json_user(request, wedding_url):
    profile = get_object_or_404(Profile, wedding_url=wedding_url)
    serializer =  UserSerializer(profile)
    return JsonResponse(serializer.data, safe=False)