from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import Question, Character, Score, Invitation, Game


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('question', 'correct_answer', 'incorret_answers')

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
    invitation = InvitationSerializer(read_only=True)
    character = CharacterSerializer(read_only=True)
    scores = ScoreSerializer(many=True)

    class Meta:
        model = Game
        fields = ('id', 'questions', 'character', 'invitation', 'scores')

class GameScoresSerializer(serializers.ModelSerializer):
    scores = ScoreSerializer(many=True)

    class Meta:
        model = Game
        fields = ('id', 'scores')

    def create_or_update_scores(self, scores):
        score_collection = []
        for score in scores:
            if 'id' not in score:
                created = Score.objects.create(**score)
                score_collection.append(created)
            else:
                score_collection.append(get_object_or_404(Score,pk=score['id']))
        return score_collection
    
    def update(self, instance, validated_data):
        scores = validated_data.pop('scores', [])
        instance.scores.set(self.create_or_update_scores(scores))
        instance.save()
        return instance