from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.contrib.auth.hashers import make_password


from .models import UserAccount
from django.contrib.auth.models import User



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)


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
    class Meta:
        model = UserAccount
        fields = ('name', 'profile_picture', 'birth_date', 'bio')


class EditProfileSerializer(serializers.ModelSerializer):
    # email = serializers.EmailField(required=False)

    class Meta:
        model = UserAccount
        fields = ('name', 'email',  'profile_picture', 'birth_date', 'bio')

    def validate_email(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError({"email": "This email is already in use."})
        return value

    def update(self, instance, validated_data):

        if validated_data['name']:
            instance.name = validated_data['name']
        if validated_data['email']:
            instance.email = validated_data['email']
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