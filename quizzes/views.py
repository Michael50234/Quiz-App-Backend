from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import get_user_model
from .models import Quiz, Tag, Question, Choice, Submission
from .serializers import QuizSerializer, CreateQuizSerializer, TagSerializer, CheckChoiceSerializer, SubmissionSerializer, CreateSubmissionSerializer, EditQuizSerializer, QuizDisplaySerializer
from .permissions import IsPublicOrOwner, IsOwner
from django.db.models import Q
from django.db import transaction


# Create your views here.

#to change: implement filtering for both UserQuizzes and Public Quizzes function

#Used to get all the users quizzes
class UserQuizzes(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        quizzes = request.user.quizzes.all()

        serializer = QuizDisplaySerializer(instance=quizzes, many=True)

        return Response(
            {
                "quizzes": serializer.data
            },
            status=200
        )
        
#Used to get all public quizzes
class PublicQuizzes(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        quizzes = Quiz.objects.filter(Q(owner=request.user) | Q(is_public=True)).distinct()

        serializer = QuizDisplaySerializer(instance=quizzes, many=True)

        return Response(
            {
                'quizzes': serializer.data
            }, 
            status=200
        )

#Used to get the information for a quiz
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

#Used to edit quizzes
class EditQuiz(APIView):
    permission_classes = [IsAuthenticated, IsOwner]

    def patch(self, request, quiz_id):
        serializer = EditQuizSerializer(request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        quiz = get_object_or_404(Quiz, id=quiz_id)
        self.check_object_permissions(request, quiz)

        with transaction.atomic():
            #update quiz fields
            quiz.title = data["title"]
            quiz.is_public = data["is_public"]
            quiz.save()

            #sync tags
            quiz.tags.set(data["tag_ids"])

            #sync questions 
            existing_q_ids = set(quiz.questions.values_list("id", flat=True))
            incoming_q_ids = {q["id"] for q in data["questions"] if "id" in q}

            Question.objects.filter(id__in=existing_q_ids - incoming_q_ids).delete()

            #update and create new questions
            for q_data in data["questions"]:
                #update existing questions
                if "id" in q_data:
                    question = Question.objects.get(id=q_data["id"], quiz=quiz)
                    question.question = q_data["question"]
                    question.save()
                #create new questions
                else:
                    question = Question.objects.create(question=q_data["question"], quiz=quiz)
            
                #sync choices
                existing_c_ids = set(question.choices.values_list("id", flat=True))
                incoming_c_ids = {choice["id"] for choice in q_data["choices"] if "id" in choice}
                
                Choice.objects.filter(id__in=existing_c_ids - incoming_c_ids).delete()

                #update and create new choices
                for c_data in q_data["choices"]:
                    if "id" in c_data:
                        choice = Choice.objects.get(question=question, id=c_data["id"])
                        choice.choice = c_data["choice"]
                        choice.is_answer = c_data["is_answer"]
                        choice.save()
                    else:
                        Choice.objects.create(choice=c_data["choice"], is_answer=c_data["is_answer"], question=question)
        
        return Response(
            {
                "detail": "Quiz updated successfully"
            },
            status=200
        )        

#Used to delete a quiz from the database
class DeleteQuiz(APIView):
    permission_classes = [IsAuthenticated, IsOwner]

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
    
#Used to create quizzes
class CreateQuiz(APIView):
    permission_classes = [IsAuthenticated]
    #create quiz
    def post(self, request):
        serializer = CreateQuizSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
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

#Returns a list of all existing tags
class TagsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = TagSerializer(instance=Tag.objects.all(), many=True)

        return Response(
            {
                'tags': serializer.data
            },
            status=200
        )

#Checks the users answer to a question
class CheckQuestion(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, choice_id):
        serializer = CheckChoiceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        is_answer = Choice.objects.get(id=choice_id).is_answer

        return Response(
            {
                'choice': serializer.validated_data.get('choice'),
                'is_answer': is_answer
            },
            status=200
        )


class SubmissionView(APIView):
    permission_classes = [IsAuthenticated]

    #Saves an attempt to the database
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
    
    #Gets the attempt history of the user
    def get(self, request):
        serializer = SubmissionSerializer(instance=request.user.submissions.all(), many=True)
        return Response(
            {
            "submissions": serializer.data
            },
            status=200
        )