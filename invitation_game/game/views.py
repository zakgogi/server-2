from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import  JsonResponse
from django.views.decorators.csrf import csrf_exempt

from pathlib import Path
import json

from .serializers import GameSerializer, GameScoresSerializer, QuestionSerializer,  UserSerializer
from .models import Question, Character, Score, Invitation, Game, Profile
from .forms import NewGameForm

script_location = Path(__file__).absolute().parent
file_location2 = script_location / 'static/game/questions.json'

with file_location2.open() as json_file:
    questionData = json.load(json_file)

# Create your views here.

user_side1_questions = []
user_side1 = None
user_side2_questions = []
user_side2 = None
user_side2_character = None
user_side1_character = None
user_invitation = None


@login_required
def update_questions(request, game = 0):
    if request.method == 'POST':
        user_questions=[]
        print(request.body.decode('utf-8'))
        form=request.POST
        for n in range(len(questionData['questions'])):
            incorrect_list = request.POST.getlist('incorrect-answer-'+str(n))
            data={
                'question':form['question-'+str(n)],
                'correct_answer': form['correct-answer-'+str(n)],
                'incorrect_answers': incorrect_list
            }
            actual = QuestionSerializer(data=data)
            if actual.is_valid():
                id=actual.save()
                user_questions.append(id)
            else:
                print(actual.errors)
        if(game==0):
            global user_side1_questions
            user_side1_questions = user_questions
        else:
            global user_side2_questions
            user_side2_questions = user_questions
        return render(request, "home", game=game)

    else:
        context = {"questions": questionData['questions']}
        return render(request, "game/chooseQuestions.html", context)

@login_required
def home(request):
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

def game(request, game):

    return render(request, 'game/new.html')
def invitation(request, game):

    return render(request, 'game/new.html')
    
def update_character(request, game):

    return render(request, 'game/new.html')

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