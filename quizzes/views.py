from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import get_user_model
from .models import Quiz
from .serializers import QuizSerializer
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
        Quiz.objects.create()
    
    def patch():
    


class SubmitQuiz(APIView):
    pass

class Submission(APIView):
    pass