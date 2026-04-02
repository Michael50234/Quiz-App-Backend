from rest_framework import serializers
from .models import Choice, Quiz, Question, Tag, Submission
from accounts.serializers import QuizUserSerializer

#quiz display serializers
class TagDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = [
            'name',
        ]

class QuizDisplaySerializer(serializers.ModelSerializer):
    tags = TagDisplaySerializer(many=True)
    owner = QuizUserSerializer()

    class Meta:
        model=Quiz
        fields = [
            'id',
            'title',
            'owner',
            'tags',
            'cover_image_url',
            'description'
        ]

#Quiz Detail View Serializers
class TagSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Tag
        fields = [
            'id',
            'name',
        ]

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = [
            'id',
            'choice',
            'is_answer'
        ]

class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True)

    class Meta:
        model = Question
        fields = [
            'id',
            'question',
            'choices',
            'question_image_url',
        ]

class QuizSerializer(serializers.ModelSerializer):
    owner = QuizUserSerializer()
    questions = QuestionSerializer(many=True)
    tags = TagSerializer(many=True)

    class Meta:
        model = Quiz
        fields = [
            'id',
            'title',
            'is_public',
            'cover_image_url',
            'description',
            'tags',
            'owner',
            'questions',
        ]

class SubmissionSerializer(serializers.ModelSerializer):
    user = QuizUserSerializer()
    quiz_title = serializers.CharField(source="quiz.title")

    class Meta:
        model = Submission
        fields = [
            'id',
            'quiz_title',
            'user',
            'submission_time',
            'score',
            'number_of_questions',
        ]

#Quiz Play Serializers
class ChoicePlaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = [
            'id',
            'choice'
        ]

class QuestionPlaySerializer(serializers.ModelSerializer):
    choices = ChoicePlaySerializer(many=True)

    class Meta: 
        model = Question
        fields = [
            'id',
            'question',
            'choices',
            'question_image_url',
        ]

class QuizPlaySerializer(serializers.ModelSerializer):
    owner = QuizUserSerializer()
    questions = QuestionPlaySerializer(many=True)

    class Meta:
        model = Quiz
        fields = [
            'id',
            'title',
            'cover_image_url',
            'owner',
            'questions',
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
    uid = serializers.CharField(max_length=1000)
    choices = CreateChoiceSerializer(many=True)
    question = serializers.CharField(max_length=400)
    question_image_url = serializers.CharField(max_length=1000, allow_null=True, default=None)

class CreateQuizSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100, default="Untitled")
    tag_ids = serializers.ListField(child=serializers.IntegerField())
    questions = CreateQuestionSerializer(many=True)
    is_public = serializers.BooleanField(default=False)
    cover_image_url = serializers.CharField(max_length=1000, default=None, allow_null=True, required=False)
    description = serializers.CharField(max_length=3000, allow_blank=True, default="")

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
    uid = serializers.CharField(max_length=1000)
    id = serializers.IntegerField(required=False)
    question = serializers.CharField()
    choices = EditChoiceSerializer(many=True)
    question_image_url = serializers.CharField(max_length=1000, allow_null=True, default=None, required=False)

class EditQuizSerializer(serializers.Serializer):
    title = serializers.CharField()
    is_public = serializers.BooleanField()
    tag_ids = serializers.ListField(child=serializers.IntegerField())
    questions = EditQuestionSerializer(many=True)
    cover_image_url = serializers.CharField(max_length=1000, default=None, allow_null=True, required=False)
    description = serializers.CharField(max_length=3000, allow_blank=True, default="")