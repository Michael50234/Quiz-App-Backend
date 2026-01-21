from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model, authenticate

# Create your views here.

class register(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        User = get_user_model()

        if User.objects.filter(username=request.data.get("username")).exists():
            return Response(
                {
                    "error": "Username already exists"
                },
                #conflict with system data ocde
                status=status.HTTP_409_CONFLICT
            )

        User.objects.create_user(username=request.data.get("username"), password=request.data.get("password"))
        user = User.objects.get(username=request.data.get("username"))

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            },
            #sign up successful code
            status=201
        )
        
class login(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user = authenticate(username=request.data.get("username"), password=request.data.get("password"))
        
        if not user:
            return Response(
                {
                    'error': "Username or password incorrect"
                },
                #not authorized to login code
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            },
            #success code
            status=200
        )
    

class logout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")
        #turns token into object
        refresh_token = RefreshToken(refresh_token)
        refresh_token.blacklist()

        #success code
        return Response(status=200)
