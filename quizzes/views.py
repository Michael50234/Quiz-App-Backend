from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import get_user_model
from .models import Quiz, Tag, Question, Choice
from .serializers import QuizSerializer, CreateQuizSerializer, TagSerializer, CheckChoiceSerializer, SubmissionSerializer, CreateSubmissionSerializer
from .permissions import IsPublicOrOwner, IsOwner
from django.db.models import Q


# Create your views here.

class UserQuizzes(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        quizzes = request.user.quizzes

        serializer = QuizSerializer(instance=quizzes, many=True)
        serializer.is_valid(raise_exception=True)

        return Response(
            {
                "quizzes": serializer.validated_data
            },
            status=
        )
        

class PublicQuizzes(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        quizzes = Quiz.objects.filter(Q(owner=request.user) | Q(is_public=True))

        serializer = QuizSerializer(instance=quizzes, many=True)
        serializer.is_valid(raise_exception=True)

        return Response(
            {
                'quizzes': serializer.validated_data
            }, 
            status=
        )


class QuizView(APIView):
    permission_classes = [IsAuthenticated, IsPublicOrOwner]

    #get quiz data
    def get(self, request, quiz_id):
        quiz = Quiz.objects.get(id=quiz_id)
        self.check_object_permissions(request, quiz)
        serializer = QuizSerializer(instance=quiz)
        serializer.is_valid()

        return Response({
            'quiz': serializer.validated_data
        },
        status=
        )
    
    #create quiz
    def post(self, request):
        serializer = CreateQuizSerializer(request.data)
        serializer.is_valid(raise_exception=True)
        quiz = Quiz(title=serializer.validated_data.get('title'), owner=request.user, is_public=serializer.validated_data.get('is_public'))
        quiz.save()
        
        for tag_id in serializer.validated_data.get('tag_ids'):
            tag = Tag.objects.filter(id=tag_id)
            quiz.add(tag)
        
        for question_object in serializer.validated_data.get('questions'):
            question = Question(question=question_object['question'], quiz=quiz)

            for choice_object in question_object['choices']:
                choice = Choice(choice=choice_object['choice'], is_answer=choice_object['is_answer'], question=question)
    
    def patch():
        pass
    
class TagsView(APIView):

    def get(self, request):
        serializer = TagSerializer(instance=Tag.objects.all(), many=True)
        serializer.is_valid()

        return Response(
            {
                'tags': serializer.validated_data
            },
            status=
        )

#The frontend will pass in the choice selected and check if it was correct
#This will return an object containing the choice selected, a answer flag, and its id
class CheckQuestion(APIView):
    def post(self, request):
        serializer = CheckChoiceSerializer(request.data)
        serializer.is_valid()

        is_answer = Choice.objects.get(id=serializer.validated_data.get('id')).is_answer

        return Response(
            {
                'id': serializer.validated_data.get('id'),
                'choice': serializer.validated_data.get('choice'),
                'is_answer': is_answer
            },
            status=
        )


class Submission(APIView):
    #adds a submission to the database
    #parameters are number of questions, score, and quiz name
    def post(self, request):
        serializer = CreateSubmissionSerializer(request.data)
        Submission.objects.create(user=request.user, score=serializer.validated_data.get('score'))
        

    #gets all submissions for the user  
    def get(self, request):
        serializer = SubmissionSerializer(request.user.submissions, many=True)
        serializer.is_valid()

        return Response(
            {
            "submissions": serializer.validated_data
            },
            status=
        )