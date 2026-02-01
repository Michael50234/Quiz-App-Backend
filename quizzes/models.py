from django.db import models
from django.conf import settings

# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=50)

class Quiz(models.Model):
    title = models.CharField(max_length=200, default="Untitled")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="quizzes")
    tags = models.ManyToManyField(Tag, related_name="tags")
    is_public = models.BooleanField(default=False)

class Question(models.Model):
    question = models.CharField(max_length=500)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    

#for each question create 4 choices and mark one as is_answer = True
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    choice = models.CharField(max_length=400)
    is_answer = models.BooleanField(default=False)


class Submission(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="submissions")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="submissions")
    submission_time = models.DateField(auto_now_add=True)
    score = models.IntegerField()
    number_of_questions = models.IntegerField()



