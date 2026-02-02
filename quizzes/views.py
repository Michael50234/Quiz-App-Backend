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
        quizzes = request.user.quizzes.all()

        serializer = QuizSerializer(instance=quizzes, many=True)

        return Response(
            {
                "quizzes": serializer.data
            },
            status=200
        )
        

class PublicQuizzes(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        quizzes = Quiz.objects.filter(Q(owner=request.user) | Q(is_public=True)).distinct()

        serializer = QuizSerializer(instance=quizzes, many=True)

        return Response(
            {
                'quizzes': serializer.data
            }, 
            status=200
        )


class QuizView(APIView):
    permission_classes = [IsAuthenticated, IsPublicOrOwner]

    #get quiz data
    def get(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, id=quiz_id)
        self.check_object_permissions(request, quiz)
        serializer = QuizSerializer(instance=quiz)

        return Response(
            {
                'quiz': serializer.data
            },
            status=200
        )

    
    #Only the quiz details like the tags, title, and public status can be updated
    def put(self, request, quiz_id):
        serializer = CreateQuizSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        quiz = get_object_or_404(Quiz, id=quiz_id)
        self.check_object_permissions(request, quiz)
        quiz.delete()

        quiz = Quiz(title=serializer.validated_data.get('title'), owner=request.user, is_public=serializer.validated_data.get('is_public'))
        quiz.save()
        
        for tag_id in serializer.validated_data.get('tag_ids'):
            tag = Tag.objects.get(id=tag_id)
            quiz.tags.add(tag)
        
        for question_object in serializer.validated_data.get('questions'):
            question = Question(question=question_object['question'], quiz=quiz)
            question.save()

            for choice_object in question_object['choices']:
                choice = Choice(choice=choice_object['choice'], is_answer=choice_object['is_answer'], question=question)
                choice.save()

        return Response(
            {
                "detail": "Successfully deleted quiz"
            },
            status=200
        )

    
    def delete(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, id=quiz_id)
        self.check_object_permissions(request, quiz)
        quiz.delete()
        return Response(
            {
                "details": "Successfully deleted quiz"
            },
            status=204
        )

        

class CreateQuiz(APIView):
    #create quiz
    def post(self, request):
        serializer = CreateQuizSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        quiz = Quiz(title=serializer.validated_data.get('title'), owner=request.user, is_public=serializer.validated_data.get('is_public'))
        quiz.save()
        
        for tag_id in serializer.validated_data.get('tag_ids'):
            tag = Tag.objects.get(id=tag_id)
            quiz.tags.add(tag)
        
        for question_object in serializer.validated_data.get('questions'):
            question = Question(question=question_object['question'], quiz=quiz)
            question.save()

            for choice_object in question_object['choices']:
                choice = Choice(choice=choice_object['choice'], is_answer=choice_object['is_answer'], question=question)
                choice.save()
        
        return Response(
            {
                "detail": "Successuflly created quiz"
            },
            status=201
        )

class TagsView(APIView):

    def get(self, request):
        serializer = TagSerializer(instance=Tag.objects.all(), many=True)

        return Response(
            {
                'tags': serializer.data
            },
            status=200
        )

#The frontend will pass in the choice selected and check if it was correct
#This will return an object containing the choice selected, a answer flag, and its id
class CheckQuestion(APIView):
    def post(self, request):
        serializer = CheckChoiceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        is_answer = Choice.objects.get(id=serializer.validated_data.get('id')).is_answer

        return Response(
            {
                'id': serializer.validated_data.get('id'),
                'choice': serializer.validated_data.get('choice'),
                'is_answer': is_answer
            },
            status=200
        )


#adjust serializers for these to account for changed model
class Submission(APIView):
    #adds a submission to the database
    #parameters are number of questions, score, and quiz id
    def post(self, request):
        serializer = CreateSubmissionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        quiz = Quiz.objects.get(id=serializer.validated_data.get("quiz_id"))
        Submission.objects.create(user=request.user, score=serializer.validated_data.get('score'), number_of_questions=serializer.validated_data.get("number_of_questions"), quiz=quiz)

        return Response(
            {
                "detail": "Successfully submitted"
            },
            status=201
        )
        

    #gets all submissions for the user  
    def get(self, request):
        serializer = SubmissionSerializer(instance=request.user.submissions.all(), many=True)
        return Response(
            {
            "submissions": serializer.data
            },
            status=200
        )