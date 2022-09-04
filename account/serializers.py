from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import InvalidToken

from django.contrib.auth.hashers import make_password


from .models import UserAccount
from relation.serializers import RelationListSerializer
from django.contrib.auth.models import User



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        print(token)

        token['username'] = user.username
        return token





class UserAccountCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True,
        style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True,
                                      style={'input_type': 'password'})


    class Meta:
        model = UserAccount
        fields = ('name', 'password','password2',  'profile_picture', 'email', 'birth_date', 'bio')
        extra_kwargs = {'password': {'write_only': True}, 'password2': {'write_only': True}}



    def validate(self, attr):
        if attr['password'] != attr['password2']:
            raise ValidationError("password must match.")
        if len(attr['password']) < 7:
            raise ValidationError("This password must contain at least 7 characters.")
        return attr

    def clean(self):
        # cleaned_data = super().clean()
        # email = cleaned_data.get('email')
        email = self.cleaned_data.get('email')

        print(email)
        if User.objects.filter(email=email).exists():
            print('errorrrrrr')
            raise ValidationError("Email exists")
        return self.cleaned_data



    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(username=validated_data['name'])
        user.set_password(password)
        user.save()
        useraccount = UserAccount.objects.create(
                                                 name=validated_data['name'],
                                                 profile_picture=validated_data['profile_picture'],
                                                 email=validated_data['email'],
                                                 birth_date=validated_data['birth_date'],
                                                 bio=validated_data['bio'])
        useraccount.username = user
        useraccount.save()
        return  useraccount

class ProfileSerializer(serializers.ModelSerializer):
    # follower = serializers.SerializerMethodField()
    # following = serializers.SerializerMethodField()
    date_joined = serializers.SerializerMethodField('get_date_joined')
    # user_image = serializers.ImageField(source='follower.profile_picture')
    followers_count = serializers.IntegerField(source='follewrs.count', read_only=True)
    followings_count = serializers.IntegerField(source='followings.count', read_only=True)

    class Meta:
        model = UserAccount
        fields = ('id', 'name','email', 'date_joined',
                  'profile_picture', 'bio', 'followers_count', 'followings_count')
    def get_date_joined(self, obj):
        date_joined = obj.username.date_joined
        return date_joined.strftime('%Y-%m-%d')

    # def get_follower(self, obj):
    #     serializer = RelationListSerializer(obj.follewrs.all(), many=True)
    #     return serializer.data[0]['from_user']

    # def get_following(self, obj):
    #     serializer = RelationListSerializer(obj.followings.all(), many=True)
    #     # print(serializer.data[0]['to_user'])
    #     return serializer.data[0]['to_user']

class EditProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserAccount
        fields = ('name',  'profile_picture', 'birth_date', 'bio')



    def update(self, instance, validated_data):

        if validated_data['name']:
            instance.name = validated_data['name']
        if validated_data['profile_picture']:
            instance.profile_picture = validated_data['profile_picture']
        if validated_data['birth_date']:
            instance.birth_date = validated_data['birth_date']
        if validated_data['bio']:
            instance.bio = validated_data['bio']

        instance.save()

        return instance



class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True,
        style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True,
                                      style={'input_type': 'password'})
    old_password = serializers.CharField(write_only=True, required=True,
                                         style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value


    def update(self, instance,validated_data):
        password = validated_data['password']
        user = User.objects.filter(username=self.instance)

        # print(password)
        for u in user:
            u.set_password(password)
            u.save()

        return u

class DeleteUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class MiniProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ('name', 'profile_picture')