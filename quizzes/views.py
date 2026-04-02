from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import get_user_model
from .models import Quiz, Tag, Question, Choice, Submission
from .serializers import QuizSerializer, CreateQuizSerializer, TagSerializer, SubmissionSerializer, CreateSubmissionSerializer, EditQuizSerializer, QuizDisplaySerializer, QuizPlaySerializer, ChoicePlaySerializer
from .permissions import IsPublicOrOwner, IsOwner
from django.db.models import Q
from django.db import transaction


# Create your views here.

#to change: implement filtering for both UserQuizzes and Public Quizzes function

#Used to get all the users quizzes
class UserQuizzes(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        quizzes = request.user.quizzes.all().distinct()

        searchText = request.query_params.get("searchText")
        tag_ids = request.query_params.getlist("tagId")

        if(searchText):
            quizzes = quizzes.filter(title__icontains=searchText)
        if(tag_ids):
            quizzes = quizzes.filter(tags__id__in=tag_ids)

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

        searchText = request.query_params.get("searchText")
        tag_ids = request.query_params.getlist("tagId")

        if(searchText):
            quizzes = quizzes.filter(title__icontains=searchText)
        if(tag_ids):
            quizzes = quizzes.filter(tags__id__in=tag_ids)

        serializer = QuizDisplaySerializer(instance=quizzes, many=True)

        return Response(
            {
                'quizzes': serializer.data
            }, 
            status=200
        )

#Used to get the information for a quiz
class QuizDetailView(APIView):
    permission_classes = [IsAuthenticated, IsPublicOrOwner]

    #get quiz data
    def get(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, id=quiz_id)
        self.check_object_permissions(request, quiz)
        serializer = QuizSerializer(instance=quiz)

        return Response(
            serializer.data,
            status=200
        )

#Used to get information for playing a quiz (doesnt return answers)
class QuizPlayView(APIView):
    permission_classes = [IsAuthenticated, IsPublicOrOwner]

    def get(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, id=quiz_id)
        self.check_object_permissions(request, quiz)
        serializer = QuizPlaySerializer(instance=quiz)

        return Response(
            serializer.data,
            status=200
        )

#Used to edit quizzes
class EditQuiz(APIView):
    permission_classes = [IsAuthenticated, IsOwner]

    def patch(self, request, quiz_id):
        serializer = EditQuizSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        quiz = get_object_or_404(Quiz, id=quiz_id)
        self.check_object_permissions(request, quiz)
        response = {"quiz_id": quiz_id, "question_ids": {}}

        with transaction.atomic():
            #update quiz fields
            quiz.title = data["title"]
            quiz.is_public = data["is_public"]
            quiz.cover_image_url = data["cover_image_url"]
            quiz.description = data["description"]
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
                    response["question_ids"][q_data["uid"]] =  q_data["id"]
                    question = Question.objects.get(id=q_data["id"], quiz=quiz)
                    question.question = q_data["question"]
                    question.question_image_url = q_data["question_image_url"]
                    question.save()
                #create new questions
                else:
                    question = Question.objects.create(question=q_data["question"], quiz=quiz, question_image_url=q_data["question_image_url"])
                    response["question_ids"][q_data["uid"]] = question.id
            
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
            response,
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
            status=204
        )
    
#Used to create quizzes
class CreateQuiz(APIView):
    permission_classes = [IsAuthenticated]
    #create quiz
    def post(self, request):
        serializer = CreateQuizSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        response = {}

        with transaction.atomic():
            quiz = Quiz(title=serializer.validated_data.get('title'), owner=request.user, is_public=serializer.validated_data.get('is_public'), cover_image_url=serializer.validated_data.get("cover_image_url"), description=serializer.validated_data.get("description"))
            quiz.save()

            response["quiz_id"] = quiz.id
            response["question_ids"] = {} 
            
            for tag_id in serializer.validated_data.get('tag_ids'):
                tag = Tag.objects.get(id=tag_id)
                quiz.tags.add(tag)
            
            for question_object in serializer.validated_data.get('questions'):
                question = Question(question=question_object['question'], quiz=quiz, question_image_url=question_object["question_image_url"])
                question.save()

                response["question_ids"][question_object["uid"]] = question.id

                for choice_object in question_object['choices']:
                    choice = Choice(choice=choice_object['choice'], is_answer=choice_object['is_answer'], question=question)
                    choice.save()
        
        return Response(
            response,
            status=201
        )

#Returns a list of all existing tags
class TagsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = TagSerializer(instance=Tag.objects.all(), many=True)

        return Response(
            {
                "tags": serializer.data
            },
            status=200
        )

#Checks the users answer to a question
class CheckQuestion(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, choice_id):
        # Use the choice id to find the id of the correct choice for the question
        choice = Choice.objects.get(id=choice_id)
        question = choice.question
        question_choices = question.choices.all()

        correct_choice_id = None

        for choice in question_choices:
            if choice.is_answer:
                correct_choice_id = choice.id
        
        #Return the id of the correct choice if it exists
        if correct_choice_id:
            return Response(
                {
                    "correct_choice_id": correct_choice_id
                },
                status=200
            )
        
        #Return an error if no correct choice exists for the question
        else:
            return Response(
                {
                    "detail": "No correct choice found"
                },
                status=status.HTTP_400_BAD_REQUEST
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