from django import forms
from .models import Character, Game, Invitation, Profile

class NewGameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['character', 'questions']
        widgets = {
            'questions': forms.HiddenInput(),
            'character': forms.HiddenInput()
        }

class NewInvitationForm(forms.ModelForm):
    class Meta:
        model = Invitation
        fields = '__all__'

class NewCharacterForm(forms.ModelForm):
    class Meta:
        model = Character
        fields = '__all__'

class NewProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        widgets = {
            'user': forms.HiddenInput(),
            'side1': forms.HiddenInput(),
            'side2': forms.HiddenInput(),
            'invitation': forms.HiddenInput()
        }