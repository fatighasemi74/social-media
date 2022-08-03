from django.shortcuts import render
from rest_framework.generics import  CreateAPIView,GenericAPIView, RetrieveUpdateAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


from .models import UserAccount

from .serializers import UserAccountCreateSerializer, MyTokenObtainPairSerializer

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserAccountCreateSerializer

    def post(self, request, *args, **kwargs):
        try:
            user = self.create(request, *args, **kwargs)
            content = {'message': 'created succesfully!'}
            return Response(content, status=status.HTTP_200_OK)
        except Exception as e:
            content = {'message': 'user already exist'}
            return Response(content, status=status.HTTP_201_CREATED)




    # def create(self, request, *args, **kwargs):
    #     response = super().create(request, *args, **kwargs)
        # serializer = UserAccountCreateSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # content = {'message': 'created succesfully!'}
        # return Response(content, status=status.HTTP_200_OK)

        # return Response({
        #     'status': 200,
        #     'message': 'Testimonials fetched',
        #     'data': response.data
        # })



class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

