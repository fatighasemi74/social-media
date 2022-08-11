from rest_framework.generics import  CreateAPIView
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.middleware import csrf
from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework import viewsets
from rest_framework import status, generics
from django.shortcuts import get_object_or_404




from .models import UserAccount
from .serializers import UserAccountCreateSerializer, MyTokenObtainPairSerializer,\
    ProfileSerializer, EditProfileSerializer, ChangePasswordSerializer



#new functions:
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }



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
                # print(username)
                data = get_tokens_for_user(user)
                data['username'] = username

                # print(data)
                response.set_cookie(
                    key = settings.SIMPLE_JWT['AUTH_COOKIE'],
                    value = data["access"],
                    expires = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                    secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                    httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                    samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
                )
                csrf.get_token(request)


                response.data = {"Success" : "Login successfully","data":data['access'], "username": data["username"]}
                return response
            else:
                return Response({"No active" : "This account is not active!!"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"Invalid" : "Invalid username or password!!"}, status=status.HTTP_404_NOT_FOUND)

# class MyTokenObtainPairView(TokenObtainPairView):
#     serializer_class = MyTokenObtainPairSerializer


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





class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)




class ProfileViewSet(viewsets.ViewSet):
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self, request, username, *args, **kwargs):
        queryset = UserAccount.objects.all()
        user = get_object_or_404(queryset, **{'name':username})
        serializer = ProfileSerializer(user)
        return Response(serializer.data)


class EditProfileView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = EditProfileSerializer

    def get_queryset(self, request, username, *args, **kwargs):
        queryset = UserAccount.objects.all()
        user = get_object_or_404(queryset, **{'name':username})
        serializer = EditProfileSerializer(user)
        return Response(serializer.data)


class ChangePasswordView(generics.UpdateAPIView):

    queryset = UserAccount.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer