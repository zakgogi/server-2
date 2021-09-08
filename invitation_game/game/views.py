from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import  JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from pathlib import Path
import json

from .serializers import GameSerializer, GameScoresSerializer, InvitationSerializer, IDGameSerializer, QuestionSerializer,  UserSerializer, QuestionSaverSerializer
from .models import Question, Character, Score, Invitation, Game, Profile
from .forms import NewGameForm, NewInvitationForm

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
def update_questions(request, game = 1):
    # 1st check if there questioons are attached to the game object_n of the profile of the user
    # generate questions with that ones and update with the request
    # update session question
    # if not: ------------------ from this done v
    #   2nd check if there are questions attached to session
    #   generate questions with that one and update with the request
    #   update session questions
    #   if not: 
    #       generate a totally new questions with the request
    #       update session questions
    
    if request.method == 'POST':
        if(game == 1):
            if "user_side1_questions" in request.session:
                user_questions = request.session["user_side1_questions"].split(',')
            else:   
                user_questions=[]
        else:
            if "user_side2_questions" in request.session:
                user_questions = request.session["user_side2_questions"].split(',')
            else:
                user_questions = []
        form=request.POST
        new_user_questions =[ ]
        for n in range(len(questionData['questions'])):
            incorrect_list = request.POST.getlist('incorrect-answer-'+str(n))
            data={
                'question':form['question-'+str(n)],
                'correct_answer': form['correct-answer-'+str(n)],
                'incorrect_answers': incorrect_list
            }
            if len(user_questions)==len(questionData['questions']):
                object= Question.objects.get(pk=user_questions[n])
                actual = QuestionSaverSerializer(object, data=data)
            else:
                actual = QuestionSerializer(data=data)
            if actual.is_valid():
                id=actual.save()
                new_user_questions.append(str(id.id))
            else:
                print(actual.errors)
        if(game == 1):
            user_questions=new_user_questions
            request.session["user_side1_questions"] = ','.join(user_questions)
            print(request.session["user_side1_questions"])
        else:
            user_questions=new_user_questions
            request.session["user_side2_questions"] = ','.join(user_questions)
        return redirect( "game-form", game=game)

    else:
        context = {"questions": questionData['questions']}
        return render(request, "game/chooseQuestions.html", context)

@login_required
def home(request):
    # 1st check if the loggded user have a profile
    # if no:
    #   2nd check if there is session information for the profile
    #   if no:
    #        render form empty
    #   if yes: 
    #       save session on a new profile for user
    # update session information
    # render form with the session information
    if request.method == 'POST':
        
        data = {
                    'side1': IDGameSerializer(user_side1),
                    'side2': IDGameSerializer(user_side2),
                    'invitation': InvitationSerializer(user_invitation),
                    'wedding_url': request.POST['wedding_url']
                }

        user = User.objects.get(username=request.user.username)
        if user.profile.id:
            profile = Profile.objects.get(pk=user.profile.id)
            print(user.profile)
            id = UserSerializer(profile, data=data)
        else:
            profile = UserSerializer(data=data)
            user.profile = Profile.objects.get(pk=profile.id)
        return redirect(request, "game/newProfile.html", data=data)        
    else:
        form = NewGameForm()
    data = {'form': form, 'questions':''}
    return render(request, 'game/newProfile.html', data)
        

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
    # 1st check if there an game in the side_n  attached to the user.profile
    # generate game with that one and update with the request
    # update session game
    # if not:
    #   2nd check if there invitation attached to session
    #   generate invitation with that one and update with the request
    #   update session invitation
    #   if not: 
    #       generate a totally new invitation with the request
    #       update session invitation

    return render(request, 'game/new.html')

def invitation(request):
    # 1st check if there an invitation attached to the user
    # generate invitation with that one and update with the request
    # update session invitation
    # if not:
    #   2nd check if there invitation attached to session
    #   generate invitation with that one and update with the request
    #   update session invitation
    #   if not: 
    #       generate a totally new invitation with the request
    #       update session invitation
    if request.method == 'POST':
        if hasattr(request.user, 'profile'):
            obj = request.user.profile.invitation
            invitationInstance = get_object_or_404(Invitation, pk=obj.id)
            invitation = NewInvitationForm(data=request.POST, instance=invitationInstance)
        else:
            if "user_invitation" in request.session:
                obj = request.session["user_invitation"]
                print(obj)
                invitationInstance = get_object_or_404(Invitation, pk=obj)
                print(invitationInstance)
                invitation = NewInvitationForm(data=request.POST, instance=invitationInstance)
            else:
                invitation = NewInvitationForm(data=request.POST)
        if invitation.is_valid():
            id=invitation.save()
            request.session["user_invitation"] = id.id
            print(request.session["user_invitation"])
            return redirect('home')
        else:
            print(invitation.errors)
            form= invitation
            data= {
                'form': form
            }
            return render(request, 'game/newInvitation.html', data)
    else :
        form= NewInvitationForm()
        data= {
            'form': form
        }
        return render(request, 'game/newInvitation.html', data)
    
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