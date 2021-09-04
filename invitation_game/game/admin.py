from django.contrib import admin
from .models import Game, Invitation, Score, Character, Question

# Register your models here.
admin.site.register(Game)
admin.site.register(Invitation)
admin.site.register(Score)
admin.site.register(Character)
admin.site.register(Question)
