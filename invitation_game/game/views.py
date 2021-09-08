from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import  JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from pathlib import Path
import json

from .serializers import CharacterSerializer, GameSerializer, GameScoresSerializer, QuestionSerializer,  UserSerializer, QuestionSaverSerializer
from .models import Question, Character, Invitation, Game, Profile
from .forms import NewGameForm, NewInvitationForm, NewProfileForm, NewCharacterForm

script_location = Path(__file__).absolute().parent
file_location2 = script_location / 'static/game/questions.json'
file_location = script_location / 'static/game/character_map.json'

with file_location.open() as json_file:
    characterData = json.load(json_file)

with file_location2.open() as json_file:
    questionData = json.load(json_file)

script_location = Path(__file__).absolute().parent

# Create your views here.

user_side1_questions = []
user_side1 = None
user_side2_questions = []
user_side2 = None
user_side2_character = None
user_side1_character = None
user_invitation = None
user_wedding_url=None


@login_required
def update_questions(request, gamenumber=1, name='user'):
    # 1st check if there questioons are attached to the game object_n
    # generate questions with that ones and update with the request
    # update session question
    # if not:
    #   2nd check if there are questions attached to session
    #   generate questions with that one and update with the request
    #   update session questions
    #   if not: 
    #       generate a totally new questions with the request
    #       update session questions
    
    if request.method == 'POST':
        if(gamenumber == 1):
            if "user_side1" in request.session:
                game = get_object_or_404(Game, pk=request.session["user_side1"])
                user_questions = []
                questions = game.questions.all()
                for row in questions:
                    user_questions.append(str(row.id))
            elif "user_side1_questions" in request.session:
                user_questions = request.session["user_side1_questions"].split(',')
            else:   
                user_questions=[]
        else:
            if "user_side2" in request.session:
                game = get_object_or_404(Game, pk=request.session["user_side2"])
                user_questions = []
                for row in game.questions:
                    user_questions.append(str(row.id))
            elif "user_side2_questions" in request.session:
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
        if(gamenumber == 1):
            user_questions=new_user_questions
            request.session["user_side1_questions"] = ','.join(user_questions)
        else:
            user_questions=new_user_questions
            request.session["user_side2_questions"] = ','.join(user_questions)
        return redirect( "game-form", gamenumber=gamenumber)

    else:
        context = {"questions": questionData['questions'], 'name':name}
        return render(request, "game/chooseQuestions.html", context)

def datageter(request):
    if "user_side1" in request.session:
            game1= request.session["user_side1"]
    else:
        game1= None  
    if "user_side2" in request.session:
        game2=request.session["user_side2"]
    else:
        game2= None
    if "user_invitation" in request.session:
        invitation=request.session["user_invitation"]
    else:
        invitation= None
    if "user_wedding_url" in request.session:
        wedding= request.session["user_wedding_url"]
    else:
        wedding= None
    data = {
        'user': request.user,
        'side1': game1,
        'side2': game2,
        'invitation': invitation,
        'wedding_url': wedding
    }
    return data
def datasetter(request, id):
    profileInstance = Profile.objects.get(pk=id) #chunk that update the form to what we know
    if profileInstance.side1: request.session["user_side1"] = profileInstance.side1.id
    if profileInstance.invitation: request.session["user_invitation"] = profileInstance.invitation.id
    if profileInstance.side2: request.session["user_side2"] = profileInstance.side2.id
    if profileInstance.wedding_url: request.session["user_wedding_url"] = profileInstance.wedding_url
    return profileInstance

@login_required
def home(request):
    # 1st check if the loggded user have a profile
    #   generate profile instance with that
    #   update instance with request
    #   update session information
    #   render form with the session information
    # if no:
    #   2nd check if request info is valid
    #       create an instance with the request
    #       join it with the user
    #       update session information
    #       render form with the session information
    #   if no:
    #        render form empty
    if request.method == 'POST':
        if hasattr(request.user, 'profile'):            
            profileInstance = Profile.objects.get(pk=request.user.profile.id)
            profile=NewProfileForm(instance=profileInstance, data=request.POST)
        else:
            profile=NewProfileForm(request.POST)
        if profile.is_valid():
            id =profile.save()
            datasetter(request,id.id)
            initial=datageter(request)
            data = {
                'form':profile,
                **initial,
            }
        else:
            print(profile.errors)
            initial=datageter(request)
            data = {
                'form':profile,
                **initial
            }
    else:
        if hasattr(request.user, 'profile'):
            profileInstance = datasetter(request,request.user.profile.id)
        initial=datageter(request)
        form = NewProfileForm(initial=initial)
        data = {
            'form':form,
            **initial
        }
    return render(request, "game/newProfile.html", data)

    #     user = User.objects.get(username=request.user.username)
    #     if user.profile.id:
    #         profile = Profile.objects.get(pk=user.profile.id)
    #         print(user.profile)
    #         id = UserSerializer(profile, data=data)
    #     else:
    #         profile = UserSerializer(data=data)
    #         user.profile = Profile.objects.get(pk=profile.id)
    #     return redirect(request, "game/newProfile.html", data=data)        
    # else:
    #     initial = {

    #     }
    #     form = NewProfileForm(initial=initial)
    # data = {'form': form, 'questions':''}
    # return render(request, 'game/newProfile.html', data)
        

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

def gamedatasetter(request, id, side):
    gameInstance = Game.objects.get(pk=id) #chunk that update the form to what we know
    if gameInstance.character: request.session["user_side"+str(side)+'_character'] = gameInstance.character.id
    if gameInstance.questions.all():
        for question in gameInstance.questions.all():
            request.session["user_side"+str(side)+'_questions'] = request.session["user_side"+str(side)+'_questions']+','+str(question.id)
    if gameInstance.id: request.session["user_side"+str(side)] = gameInstance.id
    return gameInstance

def gamedatagetter(request, side):
    if "user_side"+str(side)+"_character" in request.session:
        character= request.session["user_side"+str(side)+"_character"]
        obj = Character.objects.get(pk=character)
        character_name = obj.name
    else:
        character = None
        character_name = None
    if "user_side"+str(side)+"_questions" in request.session: questions= request.session["user_side"+str(side)+"_questions"]
    else:  questions= None

    data = {
        'character': character,
        'questions': questions,
        'character_name': character_name,
        'gamenumber':side
    }
    return data

@login_required
def game(request, gamenumber):
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
    if request.method == 'POST':
        if(gamenumber==1):
            if hasattr(request.user, 'profile') and request.user.profile.side1 :
                obj = request.user.profile.side1
                gameInstance = get_object_or_404(Game, pk=obj.id)
                data={
                    'character':int(request.POST['character']),
                    'questions':request.POST['questions'].split(',')
                }
                game = NewGameForm(data=data, instance=gameInstance)
            elif "user_side1" in request.session:
                obj = request.session["user_side1"]
                gameInstance = get_object_or_404(Game, pk=obj)     
                data={
                    'character':int(request.POST['character']),
                    'questions':request.POST['questions'].split(',')
                }                
                game = NewGameForm(data=data, instance=gameInstance)
            else:
                data={
                    'character':int(request.POST['character']),
                    'questions':request.POST['questions'].split(',')
                }    
                game = NewGameForm(data=data)
        elif gamenumber==2:
            if hasattr(request.user, 'profile') and request.user.profile.side2 :
                obj = request.user.profile.side2
                gameInstance = get_object_or_404(Game, pk=obj.id)
                data={
                    'character':int(request.POST['character']),
                    'questions':request.POST['questions'].split(',')
                }
                game = NewGameForm(data=data, instance=gameInstance)
            elif "user_side2" in request.session:
                obj = request.session["user_side2"]
                gameInstance = get_object_or_404(Game, pk=obj)
                data={
                    'character':int(request.POST['character']),
                    'questions':request.POST['questions'].split(',')
                }
                game = NewGameForm(data=data, instance=gameInstance)
            else:
                data={
                    'character':int(request.POST['character']),
                    'questions':request.POST['questions'].split(',')
                }    
                game = NewGameForm(data=data)
        if game.is_valid():
            id = game.save()
            gamedatasetter(request,id.id, gamenumber)
            return redirect('home')
        else:
            print(game.errors)
            initial = gamedatagetter(request, gamenumber)
            data = {
                'form':game,
                **initial,
            }
    else:
        if gamenumber == 1:
            if hasattr(request.user, 'profile') and request.user.profile.side1:
                gameInstance = gamedatasetter(request,request.user.profile.side1.id, gamenumber)
        else:
            if hasattr(request.user, 'profile') and request.user.profile.side2:
                gameInstance = gamedatasetter(request,request.user.profile.side2.id, gamenumber)
        initial=gamedatagetter(request, gamenumber)
        form = NewGameForm(initial=initial)
        data = {
            'form':form,
            **initial
        }
    return render(request, "game/newGame.html", data)

@login_required
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
        if hasattr(request.user, 'profile') and request.user.profile.invitation :
            obj = request.user.profile.invitation
            invitationInstance = get_object_or_404(Invitation, pk=obj.id)
            invitation = NewInvitationForm(data=request.POST, instance=invitationInstance)
        else:
            if "user_invitation" in request.session:
                obj = request.session["user_invitation"]
                invitationInstance = get_object_or_404(Invitation, pk=obj)
                invitation = NewInvitationForm(data=request.POST, instance=invitationInstance)
            else:
                invitation = NewInvitationForm(data=request.POST)
        if invitation.is_valid():
            id=invitation.save()
            request.session["user_invitation"] = id.id
            return redirect('home')
        else:
            form = invitation
            data = {
                'form': form
            }
            return render(request, 'game/newInvitation.html', data)
    else:
        form = NewInvitationForm()
        data = {
            'form': form
        }
        return render(request, 'game/newInvitation.html', data)
    
def update_character(request, gamenumber):
    # 1st check if there is a character attached to the game object_n
    # generate character with that ones and update with the request
    # update session character side_n
    # if not:
    #   2nd check if there are character attached to session
    #   generate character with that one and update with the request
    #   update session character side_n
    #   if not: 
    #       generate a totally new character with the request
    #       update session character side_n
    if request.method == 'POST':
        if(gamenumber == 1):
            if "user_side1" in request.session:
                game = get_object_or_404(Game, pk=request.session["user_side1"])
                user_character = game.character.id
            elif "user_side1_character" in request.session:
                user_character = request.session["user_side1_character"]
            else:   
                user_character=None
        else:
            if "user_side2" in request.session:
                game = get_object_or_404(Game, pk=request.session["user_side2"])
                user_character = game.character.id
            elif "user_side2_character" in request.session:
                user_character = request.session["user_side2_character"]
            else:   
                user_character=None
        if user_character:
            instance = get_object_or_404(Character, pk=user_character)
            character = NewCharacterForm(instance=instance, data=request.POST)
        else:  character = NewCharacterForm(data=request.POST) #needs change maybe forms?
        if character.is_valid():
            id = character.save()
            if(gamenumber == 1):
                request.session["user_side1_character"] = id.id
            else: request.session["user_side2_character"] = id.id
            return redirect('game-form', gamenumber=gamenumber)
        else:
            data = {
                'character': characterData, #needs change maybe forms?
                'form': character
            }
            
            return render(request, 'game/newCharacter.html', data)
    else:     
        form=NewCharacterForm()
        data = {
            'character': characterData, 
            'form':form
        }
        return render(request, 'game/newCharacter.html', data)

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