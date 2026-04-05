from rest_framework import serializers
from .models import User

#create serializers for objects that will be returned (model) and to process inputs from requests (serializer)

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

#Adjust this in the quiz serializers
class QuizUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'nickname',
            'profile_picture_url',
            'about_me'
        ]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'nickname',
            'profile_picture_url',
            'about_me'
        ]

class UpdateUserSerializer(serializers.Serializer):
    nickname = serializers.CharField(max_length=50, required=False, allow_blank=True)
    profile_picture_url = serializers.CharField(max_length=1000, required=False, allow_blank=True, allow_null=True)
    about_me = serializers.CharField(max_length=3000, required=False, allow_blank=True)