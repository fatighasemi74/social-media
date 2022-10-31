import jwt
from rest_framework.generics import  CreateAPIView
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import viewsets
from rest_framework import status, generics
from django.middleware import csrf
from django.contrib.auth import authenticate
from django.conf import settings
from django.views import View
from django.shortcuts import redirect
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.contrib.auth.models import User
import datetime

from content.models import Post
from content.serializers import PostSerializer
from content.views import Pagination

from .models import UserAccount, Relation
from .serializers import UserAccountCreateSerializer, MyTokenObtainPairSerializer,\
    ProfileSerializer, CreateOrDeleteRelationSerializer, FollowingListSerializer, FollowerListSerializer


# new functions:
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
        print('hereeeeeeeeeeeeeee')
        refresh = self.request.COOKIES.get('refresh_token')
        print('refresh', refresh)
        decode = jwt.decode(refresh, settings.SECRET_KEY, algorithms='HS256')
        user_id = decode['user_id']
        username = decode['username']
        user = User.objects.filter(id=user_id).first()
        print('userrrrrrr', user)

        access = jwt.encode({
            'user_id': user_id,
            'username': username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
        }, 'SECRET_KEY', algorithm='HS256')

        data = {
            "access_token": access,
            "message": "ok",
            "status": status.HTTP_200_OK
        }

        return Response(data, status=status.HTTP_200_OK)


class LoginView(APIView):
    '''
        log in
    '''

    def post(self, request, format=None):
        data = request.data
        response = Response()
        username = data.get('username', None)
        password = data.get('password', None)
        if username and password != "":
            user = authenticate(username=username, password=password)
            useraccount = UserAccount.objects.filter(username=user).first()
            if user is not None:
                if useraccount.allowed:
                    if user.is_active:

                        username = data.get('username', None)
                        data = get_tokens_for_user(user)
                        data['username'] = username
                        response.set_cookie(
                            key = settings.SIMPLE_JWT['AUTH_COOKIE'],
                            value = data["refresh"],
                            expires = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                            secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                            httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                            samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
                        )
                        csrf.get_token(request)
                        # response.data = {"Success" : "Login successfully","data":data['access']}
                        content = {"message" : "با موفقیت وارد شدید.", "data": data['access'], 'status': 200}
                        # return response
                        return Response(content, status=status.HTTP_200_OK)
                    else:
                        content = {'message': 'کاربری هنوز فعال نشده است.', 'status': 404}
                        return Response(content, status=status.HTTP_404_NOT_FOUND)
                else:
                    content = {'message': 'کاربری هنوز تایید نشده است.', 'status': 404}
                    return Response(content, status=status.HTTP_404_NOT_FOUND)

            else:
                content = {'message': 'نام کاربری یا رمز عبور اشتباه ست.', 'status': 404}
                return Response(content, status=status.HTTP_404_NOT_FOUND)
        else:
            content = {'message': 'نام کاربری یا رمز عبور خالی ست.', 'status': 404}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserCreateAPIView(CreateAPIView):
    '''
        register with name, email, passsword and password confirmation
    '''
    serializer_class = UserAccountCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        username = serializer.data['name']
        domain = get_current_site(self.request).domain
        link = reverse('activate', kwargs={'username': username})
        activate_url = 'http://'+domain+link
        email_body = 'hii '+username+' please click the link bellow:\n' + activate_url
        email = EmailMessage(
            'subject',
            email_body,
            settings.EMAIL_HOST_USER,
            [serializer.data['email']],
        )
        email.fail_silently=False
        email.send()

class VerificationView(View):
    '''
        email link verification for log in
    '''
    def get(self, request, username):
        user = UserAccount.objects.filter(name=username).first()
        user.allowed = True
        user.save()
        return redirect('login')


class LogoutView(APIView):
    '''
        log out
    '''
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
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)




class ProfileViewSet(viewsets.ModelViewSet):
    '''
        this viewset works for list of users, user profile, edit profile, change password and for deleting account
    '''

    lookup_field = 'name'
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated, )
    queryset = UserAccount.objects.all()

    def get_queryset(self, *args, **kwargs):
        '''
            list of users, user profile
        '''
        users = UserAccount.objects.all()
        return  users


    def update(self, request, *args, **kwargs):
        '''
            edit profile, change password
        '''
        log_in = UserAccount.objects.get(name=self.request.user)
        if self.kwargs.get('name'):
            user = UserAccount.objects.get(name=self.kwargs.get('name'))
            if log_in == user:
                instance = self.get_object()
                if request.data.get('profile_picture'):
                    instance.profile_picture = request.data.get('profile_picture')
                    instance.save()
                if request.data.get('bio'):
                    instance.bio = request.data.get('bio')
                    instance.save()
                if request.data.get('birth_date'):
                    instance.birth_date = request.data.get('birth_date')
                    instance.save()
                if request.data.get('password') or request.data.get('password2'):
                    old_password = request.data.get('old_password')
                    if old_password:
                        user = self.request.user
                        if not user.check_password(old_password):
                            raise ValidationError({'message': 'پسورد قدیمی درست نیست.', 'status': 400})
                        password = request.data.get('password')
                        password2 = request.data.get('password2')
                        if password == password2 == old_password:
                            raise ValidationError({"message": "پسورد مشابه قبلی است.", 'status': 400})
                        elif password == password2:
                            user.set_password(password)
                            user.save()
                        else:
                            raise ValidationError({"message": "پسوردها یکی نیستند.", 'status': 400})
                    else:
                        raise ValidationError({"message": "پسورد قدیمی را وارد کنید.", 'status': 400})

                serializer = ProfileSerializer(instance, context={'request': request})
                return Response(serializer.data)
            else:
                content = {'message': 'پروفایل متعلق به شما نیست.', 'status': 400}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        '''
            delete account
        '''
        log_in = UserAccount.objects.get(name=self.request.user)
        if self.kwargs.get('name'):
            user = UserAccount.objects.get(name=self.kwargs.get('name'))
            if log_in == user:
                mainuser = User.objects.filter(username=user)
                mainuser.delete()
                content = {'message': 'پاک شد.'}
                return Response(content, status=status.HTTP_200_OK)
            else:
                content = {'message': 'نمیتوانید پاک کنید.'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)


class ListPostViewSet(viewsets.ModelViewSet):
    '''
        home page and explore, based on following people
    '''
    permission_classes = (IsAuthenticated, )
    serializer_class = PostSerializer
    pagination_class = Pagination
    queryset = Post.objects.all()

    def get_queryset(self):
        qs = super().get_queryset()
        username = self.request.user
        user = UserAccount.objects.filter(name=username).first()
        param = self.request.GET.get('route')
        if param == "home":
            relations = Relation.objects.filter(from_user=user.id).all()
            if relations:
                for relation in relations:
                    post = Post.objects.filter(user=relation.to_user)
                    return post
            raise ValidationError({"message": "چیزی برای نمایش وجود ندارد."})
        elif param == "explore":
            relations = Relation.objects.filter(from_user=user.id).all()
            if relations:
                for relation in relations:
                    post = Post.objects.exclude(user=relation.to_user)
                    return post
            return qs






class RelationViewSet(viewsets.ModelViewSet):
    '''
        this viewset works for list of relations, create relation and delete it.
    '''
    queryset = Relation.objects.all()
    serializer_class = CreateOrDeleteRelationSerializer
    permission_classes = [IsAuthenticated, ]
    lookup_field = 'user'


    def get_queryset(self, *args, **kwargs):
        '''
            list of relations, home
        '''
        relations = Relation.objects.all()
        return  relations

    def create(self, request, *args, **kwargs):
        '''
            create relation(follow)
        '''
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        '''
            create final def
        '''
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        '''
            delete relation(unfollow)
        '''
        to_user = UserAccount.objects.filter(name=kwargs['user']).first()
        log_in = UserAccount.objects.filter(name=request.user).first()
        relation = Relation.objects.filter(from_user=log_in,to_user=to_user).first()
        if relation:
            relation.delete()
            content = {'message': 'پاک شد.'}
            return Response(content,status=status.HTTP_200_OK)
        else:
            if to_user == log_in:
                raise ValidationError({"message": "نمیتوانید خودتان را آنفالو کنید."})
            raise ValidationError({'message': 'چیزی برای آنفالو کردن وجود ندارد.'})


class FollowingAPIView(generics.ListAPIView):
    '''
        list of following users
    '''
    serializer_class = FollowingListSerializer
    permission_classes = (IsAuthenticated, )
    queryset = Relation.objects.all()
    pagination_class = Pagination
    lookup_url_kwarg = 'username'


    def get_queryset(self):
        username = self.kwargs[self.lookup_url_kwarg]
        user = UserAccount.objects.filter(name=username).first()
        qs = Relation.objects.filter(from_user=user.id)
        return qs.filter(from_user=user.id)

class FollowerAPIView(generics.ListAPIView):
    '''
        list of follower users
    '''
    serializer_class = FollowerListSerializer
    permission_classes = (IsAuthenticated, )
    queryset = Relation.objects.all()
    pagination_class = Pagination
    lookup_url_kwarg = 'username'


    def get_queryset(self):
        username = self.kwargs[self.lookup_url_kwarg]
        user = UserAccount.objects.filter(name=username).first()
        qs = Relation.objects.filter(to_user=user.id)
        return qs.filter(to_user=user.id)


