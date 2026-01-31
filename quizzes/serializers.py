from rest_framework import serializers
from .models import Choice, Quiz, Question, Tag, Submission
from accounts.serializers import UserSerializer

#create serializers for objects that will be returned (model) and to process inputs from requests (serializer)

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = [
            'name'
        ]

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = [
            'is_answer',
            'choice'
        ]


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(source="choices", many=True)

    class Meta:
        model = Question
        fields = [
            'question',
            'choices'
        ]

class QuizSerializer(serializers.ModelSerializer):
    tags = TagSerializer(source="tags", many=True)
    owner = UserSerializer(source="owner")
    questions = QuestionSerializer(source="questions", many=True)

    class Meta:
        model = Quiz
        fields = [
            'id',
            'title',
            'tags',
            'owner',
            'questions'
        ]


class SubmissionSerializer(serializers.ModelSerializer):
    user = UserSerializer(source="user")

    class Meta:
        model = Submission
        fields = [
            'user',
            'submission_time',
            'score'
        ]

class CreateChoiceSerializer(serializers.Serializer):
    choice = serializers.CharField(max_length=400)
    is_answer = serializers.BooleanField()

class CreateQuestionSerializer(serializers.Serializer):
    choices = CreateChoiceSerializer(many=True)
    question = serializers.CharField(max_length=400)

#owner will come from request.user
#tag_ids will be inputted as an array of tag ids
class CreateQuizSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100, default="Untitled")
    tag_ids = serializers.ListField(child=serializers.IntegerField())
    questions = CreateQuestionSerializer(many=True)
    is_public = serializers.BooleanField

