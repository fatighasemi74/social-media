from rest_framework.generics import  CreateAPIView
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken , AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.middleware import csrf
from django.contrib.auth import authenticate
from django.conf import settings
from django.contrib.auth import logout
from rest_framework import viewsets
from rest_framework import status, generics
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail


from django.contrib.auth.models import User

import jwt

from .models import UserAccount
from .serializers import UserAccountCreateSerializer, MyTokenObtainPairSerializer,\
    ProfileSerializer, EditProfileSerializer, ChangePasswordSerializer, DeleteUserSerializer
from content.models import Post
from relation.models import Relation
from relation.permissions import RelationExists
from content.serializers import PostDetailSerializer, PostListSerializer


#new functions:
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    refresh['username'] = str(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def refresh_token_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'access': str(refresh.access_token),
    }

class RefreshTokenAPIView(APIView):

    def post(self, request):
        refresh = self.request.COOKIES.get('refresh_token')
        response = Response()
        decode = jwt.decode(refresh,settings.SECRET_KEY, algorithms=['HS256'])
        user_id = decode['user_id']
        user = User.objects.filter(id=user_id).first()
        data = refresh_token_for_user(user)

        print(data['access'])
        return Response(data, status=status.HTTP_200_OK)


class LoginView(APIView):

    def post(self, request, format=None):
        data = request.data
        response = Response()
        username = data.get('username', None)
        password = data.get('password', None)
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                username = data.get('username', None)
                data = get_tokens_for_user(user)
                data['username'] = username
                # print(data['refresh'])
                response.set_cookie(
                    key = settings.SIMPLE_JWT['AUTH_COOKIE'],
                    value = data["refresh"],
                    expires = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                    secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                    httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                    samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
                )
                csrf.get_token(request)
                # print(data['access'])
                response.data = {"Success" : "Login successfully","data":data['access']}
                return response
            else:
                return Response({"No active" : "This account is not active!!"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"Invalid" : "Invalid username or password!!"}, status=status.HTTP_404_NOT_FOUND)

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserAccountCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

        # name = serializer.data['name']
        # subject = 'welcome to our website!!'
        # message = f'Hi {name}, thank you for registering in here.'
        # email_form = settings.EMAIL_HOST_USER
        # recipient_list = [serializer.data['email'], ]
        # send_mail( subject, message, email_form, recipient_list, fail_silently=False)
        # print(serializer.data)




class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            response = Response()
            refresh_token = request.data.get("refresh_token")
            token = RefreshToken(refresh_token)
            token.blacklist()
            for cookie in request.COOKIES:
                response.delete_cookie(cookie)
            return response

            # return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)




class ProfileViewSet(viewsets.ViewSet):
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated, )#RelationExists)

    def get_queryset(self, request, username, *args, **kwargs):
        queryset = UserAccount.objects.all()
        user = get_object_or_404(queryset, **{'name':username})
        serializer = ProfileSerializer(user)
        return Response(serializer.data)


class EditProfileView(generics.UpdateAPIView):
    '''
        owner profile must be edited
    '''
    permission_classes = (IsAuthenticated, )
    serializer_class = EditProfileSerializer
    queryset = UserAccount.objects.all()



    def put(self, request, username, *args, **kwargs):
        queryset = UserAccount.objects.all()
        log_in = UserAccount.objects.get(username=request.user)
        user = get_object_or_404(queryset, **{'name':username})

        if user == log_in:
            serializer = EditProfileSerializer(user)
            print(serializer.data)
            return self.update(request, *args, **kwargs)
        else:
            content = {'message': 'this is not your profile'}
            return Response(content,status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(generics.UpdateAPIView):

    queryset = UserAccount.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer


    def put(self, request, pk, *args, **kwargs):
        queryset = UserAccount.objects.all()
        log_in = UserAccount.objects.get(username=request.user)
        user = get_object_or_404(queryset, **{'pk': pk})
        # print(log_in)
        # print(user)
        if user == log_in:
            serializer = EditProfileSerializer(user)
            return self.update(request, *args, **kwargs)
        else:
            content = {'message': 'you dont have the permission'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)


class DeleteUserAPIView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = DeleteUserSerializer
    queryset = UserAccount.objects.all()

    def delete(self, request, pk, *args, **kwargs):
        queryset = User.objects.all()
        log_in = User.objects.get(username=request.user)
        user = get_object_or_404(queryset, **{'pk': pk})
        print(log_in)
        print(user)
        if user == log_in:
            return self.destroy(request, *args, **kwargs)
        else:
            content = {'message': 'you cant delete'}
            return Response(content,status=status.HTTP_400_BAD_REQUEST)

class FollowingPostsAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = PostListSerializer
    queryset = UserAccount.objects.all()

    def get_queryset(self):
        qs = super().get_queryset()
        username = self.request.user
        user = UserAccount.objects.filter(name=username).first()
        relations = Relation.objects.filter(from_user=user.id).all()
        for relation in relations:
            post = Post.objects.filter(user=relation.to_user)
            return post

