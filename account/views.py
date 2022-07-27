from django.shortcuts import render
from rest_framework.generics import  CreateAPIView, RetrieveUpdateAPIView, UpdateAPIView

from rest_framework.permissions import IsAuthenticated

from .models import UserAccount
from .serializers import UserAccountCreateSerializer

class UserCreateAPIView(CreateAPIView):
    serializer_class = UserAccountCreateSerializer

# class UserLoginAPIView()
