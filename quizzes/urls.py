from django.urls import path
from . import views
#UserQuizzes, PublicQuizzes, QuizView, CreateQuiz, TagsView, CheckQuestion, Submission

urlpatterns = [
    path('user-quizzes', views.UserQuizzes.as_view(), name="user-quizzes" ),
    path('public-quizzes', views.PublicQuizzes.as_view(), name="public-quizzes"),
    path('quiz/<int:quiz_id>', views.QuizView.as_view(), name="view-quiz"),
    path('quiz/<int:quiz_id>', views.EditQuiz.as_view(), name="edit-quiz"),
    path('create-quiz', views.CreateQuiz.as_view(), name="create-quiz"),
    path('tags', views.TagsView.as_view(), name="tags"),
    path('check-question/<int:choice_id>', views.CheckQuestion.as_view(), name="check-question"),
    path('submission', views.SubmissionView.as_view(), name="submission")
]