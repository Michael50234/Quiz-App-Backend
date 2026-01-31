from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model, authenticate
from .serializers import LoginSerializer

# Create your views here.

class Register(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        User = get_user_model()
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)


        if User.objects.filter(username=serializer.validated_data.get("username")).exists():
            return Response(
                {
                    "detail": "Username already exists"
                },
                #conflict with system data ocde
                status=status.HTTP_409_CONFLICT
            )

        user = User.objects.create_user(username=serializer.validated_data.get("username"), password=serializer.validated_data.get("password"))

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            },
            #sign up successful code
            status=201
        )
        
class Login(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(username=serializer.validated_data.get("username"), password=serializer.validated_data.get("password"))
        
        if not user:
            return Response(
                {
                    'detail': "Username or password incorrect"
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
    

class Logout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response(
                {
                    'detail': "Refresh token not attached"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        #turns token into object
        try:
            refresh_token = RefreshToken(refresh_token)
            refresh_token.blacklist()
        except:
            return Response(
            {
                'detail': "Refresh token expired or invalid"
            },
            status=status.HTTP_400_BAD_REQUEST)

        #success code
        return Response(status=200)
