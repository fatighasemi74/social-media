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
from .serializers import UserAccountCreateSerializer, MyTokenObtainPairSerializer, ProfileSerializer



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
        # print(response)

        if user is not None:
            if user.is_active:
                data = get_tokens_for_user(user)
                response.set_cookie(
                    key = settings.SIMPLE_JWT['AUTH_COOKIE'],
                    value = data["access"],
                    expires = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                    secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                    httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                    samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
                )
                # print(request.COOKIES)
                csrf.get_token(request)
                # data = data['access']
                # print(data)

                response.data = {"Success" : "Login successfully","data":data['access']}
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
    # print('log out')

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            token = RefreshToken(refresh_token)
            token.blacklist()
            # print(token)
            # print('log out')

            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


# class UserProfileView(generics.RetrieveAPIView):
#
#     permission_classes = (IsAuthenticated,)
#
#
#
#     def get(self, request, pk, *args, **kwargs):
#         try:
#             user_profile = UserAccount.objects.filter(id=pk)
#             print(user_profile)
#             status_code = status.HTTP_200_OK
#             response = {
#                 'success': 'true',
#                 'status code': status_code,
#                 'message': 'User profile fetched successfully',
#                 'data': [{
#                     'name': user_profile.username,
#                     # 'bio': user_profile.bio,
#                     # 'email': user_profile.email,
#                     # 'birth_date': user_profile.birth_date,
#                     # 'profile_picture': user_profile.profile_picture,
#                     }]
#                 }
#             return Response(response, status=status_code)
#         except Exception as e:
#             status_code = status.HTTP_400_BAD_REQUEST
#             response = {
#                 'success': 'false',
#                 'status code': status.HTTP_400_BAD_REQUEST,
#                 'message': 'User does not exists',
#                 'error': str(e)
#                 }
#         return Response(response, status=status_code)

class ProfileViewSet(viewsets.ViewSet):
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self, request, pk=None):
        queryset = UserAccount.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = ProfileSerializer(user)
        return Response(serializer.data)