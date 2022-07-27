from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import UserAccount
from django.contrib.auth.models import User

class UserAccountCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True,
        style={'input_type': 'password'})
    # password = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = UserAccount
        fields = ('name', 'password',  'profile_picture', 'email', 'birth_date', 'bio')
        extra_kwargs = {'password': {'write_only': True}}

    def get_password(self, password):
        return password

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


    def validate_password(self, password):
        if len(password) < 7:
            raise ValidationError("This password must contain at least 7 characters.")