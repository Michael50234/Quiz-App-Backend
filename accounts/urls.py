from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path
from . import views

urlpatterns = [
    path("refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("login", views.Login.as_view(), name="Login"),
    path("register", views.Register.as_view(), name="Register"),
    path("logout", views.Logout.as_view(), name="Logout")
]