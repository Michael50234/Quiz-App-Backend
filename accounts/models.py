from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    nickname = models.CharField(max_length=50, blank=True)
    profile_picture_url = models.CharField(max_length=1000, null=True, default=None)
    about_me = models.CharField(max_length=3000, blank=True)
    