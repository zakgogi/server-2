from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import  JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .serializers import GameSerializer, GameScoresSerializer
from .models import Question, Character, Score, Invitation, Game

# Create your views here.
def home(req, name = 'person'):
        context = {"name": name}
    
        return render(req, "game/index.html", context)
        
def not_found_404(request, exception):
    data = { 'err': exception }
    return render(request, 'game/404.html', data)

def server_error_500(request):
    return render(request, 'game/500.html')

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
    elif request.method == 'PUT':
        
        game = get_object_or_404(Game, pk=id) 
        serializer = GameScoresSerializer(game, data=json.loads(request.body))
        if serializer.is_valid():
            print('saved')
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.data, safe=False)    