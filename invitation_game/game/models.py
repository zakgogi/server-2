from django.db import models
from django.core.validators import MinLengthValidator
from django.db.models.fields import CharField
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField



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
    hair_id = models.IntegerField()
    skin_id = models.IntegerField()
    dress_id = models.IntegerField()
    eyes_id = models.IntegerField()
    
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
    questions =models.ManyToManyField(Question, blank=True)
    character = models.ForeignKey(Character, on_delete=models.SET_NULL, null=True)
    invitation = models.ForeignKey(Invitation, on_delete=models.SET_NULL, null=True)
    scores = models.ManyToManyField(Score, blank=True)

    class Meta:
        verbose_name_plural = "games"