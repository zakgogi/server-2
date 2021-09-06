from django.db import models
from django.core.validators import MinLengthValidator
from django.db.models.fields import CharField
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

from pathlib import Path
import json

script_location = Path(__file__).absolute().parent
file_location = script_location / 'static/game/character_map.json'
file_location2 = script_location / 'static/game/questions.json'

with file_location.open() as json_file:
    characterData = json.load(json_file)
   
def character_list_tuple(data):
    lista = []
    for value in data:
        lista.append((value['id'], value['title']))
    return lista

# def question_conversor(data):

#     return lista

# Create your models here.
class Question(models.Model):
    question = models.CharField(max_length=500)
    correct_answer = models.CharField(max_length=100)
    incorret_answers = ArrayField(
        models.CharField(max_length=100, blank=True),
        size=3,
    )
    class Meta:
        verbose_name_plural = "questions"

class Character(models.Model):
    name = models.CharField(max_length=100)
    hair_id = models.IntegerField(choices=character_list_tuple(characterData['hair']))
    skin_id = models.IntegerField(choices=character_list_tuple(characterData['skin']))
    dress_id = models.IntegerField(choices=character_list_tuple(characterData['dress']))
    eyes_id = models.IntegerField(choices=character_list_tuple(characterData['eyes']))
    
    class Meta:
        verbose_name_plural = "characters"

class Score(models.Model):
    name = models.CharField(max_length=100)
    score = models.IntegerField()

    class Meta:
        verbose_name_plural = "scores"

class Invitation(models.Model):
    title = models.CharField(max_length=300)
    message = models.CharField(max_length=500)

    class Meta:
        verbose_name_plural = "invitations"

class Game(models.Model):
    date =  models.DateField(default=timezone.now)
    host_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    questions = models.ManyToManyField(Question, blank=True)
    character = models.ForeignKey(Character, on_delete=models.SET_NULL, null=True)
    invitation = models.ForeignKey(Invitation, on_delete=models.SET_NULL, null=True)
    scores = models.ManyToManyField(Score, blank=True)

    class Meta:
        verbose_name_plural = "games"