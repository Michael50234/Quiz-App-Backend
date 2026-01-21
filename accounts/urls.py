from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path
from . import views

urlpatterns = [
    path("refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("login", views.login.as_view(), name="login"),
    path("register", views.register.as_view(), name="register"),
    path("logout", views.logout.as_view(), name="logout")
]