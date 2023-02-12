from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .serializers import UserValidateSerializer, UserCreateSerializer
from rest_framework.views import APIView

class LoginAPIView(APIView):
    def post(self, request):
        serializer = UserValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response(data={'token': token.key})
        return Response(status=status.HTTP_403_FORBIDDEN)

class RegistrationAPIView(APIView):
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = request.data.get('username')
        password = request.data.get('password')
        User.objects.create_user(username=username, password=password)
        return Response(status=status.HTTP_201_CREATED)

