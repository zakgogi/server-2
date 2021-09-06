from django import forms
from .models import Game

class NewGameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['character', 'questions']
        widgets = {'owner': forms.HiddenInput()}