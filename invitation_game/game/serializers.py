from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import Question, Character, Score, Invitation, Game, Profile
from django.contrib.auth.models import User


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('question', 'correct_answer', 'incorrect_answers')

class InvitationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Invitation
        fields = ('title', 'message')

class CharacterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Character
        fields = ('name', 'hair_id', 'skin_id', 'dress_id', 'eyes_id')

class ScoreSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        model = Score
        fields = ('id','name', 'score')

class GameSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)
    character = CharacterSerializer(read_only=True)
    scores = ScoreSerializer(many=True)

    class Meta:
        model = Game
        fields = ('id', 'questions', 'character', 'scores')

class GameScoresSerializer(serializers.ModelSerializer):
    scores = ScoreSerializer(many=True)

    class Meta:
        model = Game
        fields = ('id', 'scores')

    # def create_or_update_scores(self, scores):
    #     score_collection = []
    #     for score in scores:
    #         if 'id' not in score:
    #             created = Score.objects.create(**score)
    #             score_collection.append(created)
    #         else:
    #             score_collection.append(get_object_or_404(Score,pk=score['id']))
    #     return score_collection
    
    def update(self, instance, validated_data):
        scores = validated_data.pop('scores', [])
        instance.scores.add(Score.objects.create(**scores[0]))
        instance.save()
        return instance

class IDGameSerializer(serializers.ModelSerializer):
    character = CharacterSerializer(read_only=True)

    class Meta:
        model = Game
        fields = ('id', 'character')



class UserSerializer(serializers.ModelSerializer):
    side1 = IDGameSerializer(read_only=True)
    side2 = IDGameSerializer(read_only=True)
    invitation = InvitationSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ('wedding_url', 'side1', 'side2', 'invitation')


        
