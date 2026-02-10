from rest_framework import serializers
from .models import Choice, Quiz, Question, Tag, Submission
from accounts.serializers import UserSerializer

#quiz display serializers
class TagDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = [
            'name'
        ]

class QuizDisplaySerializer(serializers.ModelSerializer):
    tags = TagDisplaySerializer(source='tags', many=True)
    owner = UserSerializer(source='owner')

    class Meta:
        model=Quiz
        fields = [
            'id'
            'title',
            'owners',
            'tags'
        ]

#quiz play serializers
class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = [
            'id'
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
    tags = TagDisplaySerializer(source="tags", many=True)
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
    quiz_title = serializers.CharField(source="quiz.title")

    class Meta:
        model = Submission
        fields = [
            'quiz_title',
            'user',
            'submission_time',
            'score',
            'number_of_questions'
        ]


#Used to return all existing tags
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model=Tag
        fields=[
            'name',
            'id'
        ]

#Creation serializers
class CreateChoiceSerializer(serializers.Serializer):
    choice = serializers.CharField(max_length=400)
    is_answer = serializers.BooleanField()

class CreateQuestionSerializer(serializers.Serializer):
    choices = CreateChoiceSerializer(many=True)
    question = serializers.CharField(max_length=400)

class CreateQuizSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100, default="Untitled")
    tag_ids = serializers.ListField(child=serializers.IntegerField())
    questions = CreateQuestionSerializer(many=True)
    is_public = serializers.BooleanField()

class CheckChoiceSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    choice = serializers.CharField(max_length=1000)

class CreateSubmissionSerializer(serializers.Serializer):
    quiz_id = serializers.IntegerField()
    score = serializers.CharField(max_length=10)
    number_of_questions = serializers.IntegerField()

#Editing serializers
class EditChoiceSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    choice = serializers.CharField()
    is_answer = serializers.BooleanField()

class EditQuestionSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    question = serializers.CharField()
    choices = EditChoiceSerializer(many=True)

class EditQuizSerializer(serializers.Serializer):
    title = serializers.CharField()
    is_public = serializers.BooleanField()
    tag_ids = serializers.ListField(child=serializers.IntegerField())
    questions = EditQuestionSerializer(many=True)