from django import forms
from .models import Game, Invitation

class NewGameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['character', 'questions']
        widgets = {'questions': forms.HiddenInput()}

class NewInvitationForm(forms.ModelForm):
    class Meta:
        model = Invitation
        fields = '__all__'