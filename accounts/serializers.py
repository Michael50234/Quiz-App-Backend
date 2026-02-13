from rest_framework import serializers
from .models import User

#create serializers for objects that will be returned (model) and to process inputs from requests (serializer)

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'nickname'
        ]

class SetNicknameSerializer(serializers.Serializer):
    nickname = serializers.CharField(max_length=50)