from rest_framework import serializers
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


    def create(self, validated_data):
        # print(validated_data)
        password = validated_data.pop('password')
        user = User.objects.create_user(validated_data['name'])
        name = validated_data['name']
        useraccount = UserAccount.objects.create(name=name)
        user.set_password(password)
        user.save()
        # useraccount.save()
        return  useraccount


    # def create_useraccount(self, validated_data):
    #     print(validated_data)
    #     return validated_data

    def get_password(self, password):
        return password
    #
    # def validate_password(self, password, user=None):
    #     if len(password) < self.min_length:
    #         raise ValidationError(
    #             _("This password must contain at least %(min_length)d characters."),
    #             code='password_too_short',
    #             params={'min_length': self.min_length},
    #         )