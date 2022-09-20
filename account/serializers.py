from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import InvalidToken

from django.contrib.auth.hashers import make_password


from .models import UserAccount, Relation
from relation.serializers import RelationListSerializer
from .functions import get_access_token
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
        fields = ('name', 'password','password2', 'email')
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
                                                 # profile_picture=validated_data['profile_picture'],
                                                 email=validated_data['email'],)
                                                 # birth_date=validated_data['birth_date'],
                                                 # bio=validated_data['bio'])
        useraccount.username = user
        # print(useraccount.allowed)
        useraccount.save()
        return  useraccount

class ProfileSerializer(serializers.ModelSerializer):
    # follower = serializers.SerializerMethodField()
    # following = serializers.SerializerMethodField()
    date_joined = serializers.SerializerMethodField('get_date_joined')
    # user_image = serializers.ImageField(source='follower.profile_picture')
    followers_count = serializers.IntegerField(source='follewrs.count', read_only=True)
    followings_count = serializers.IntegerField(source='followings.count', read_only=True)
    # is_followed = serializers.SerializerMethodField('get_is_followed')
    password = serializers.CharField(write_only=True, required=True,
        style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True,
                                      style={'input_type': 'password'})
    old_password = serializers.CharField(write_only=True, required=True,
                                         style={'input_type': 'password'})

    class Meta:
        model = UserAccount
        fields = ('id', 'name','email', 'date_joined',
                  'profile_picture', 'bio', 'followers_count', 'followings_count', 'birth_date',
                  'old_password', 'password', 'password2')

    def get_date_joined(self, obj):
        date_joined = obj.username.date_joined
        return date_joined.strftime('%Y-%m-%d')






    # def get_is_followed(self, obj):
    #     get_access_token(self.context['request'])
    #     print(obj, 'hiiii obj')

    # def get_follower(self, obj):
    #     serializer = RelationListSerializer(obj.follewrs.all(), many=True)
    #     return serializer.data[0]['from_user']

    # def get_following(self, obj):
    #     serializer = RelationListSerializer(obj.followings.all(), many=True)
    #     # print(serializer.data[0]['to_user'])
    #     return serializer.data[0]['to_user']




class MiniProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ('name', 'profile_picture', 'is_following')

class CreateOrDeleteRelationSerializer(serializers.ModelSerializer):

    from_user = serializers.CharField(source='from_user.username')
    to_user = serializers.CharField(source='to_user.username')

    class Meta:
        model = Relation
        fields = ("to_user", "from_user",)

    def create(self, validated_data):
        log_in = UserAccount.objects.filter(name=self.context['request'].user).first()
        validatedata_to_user = validated_data['to_user']
        userto = validatedata_to_user['username']
        to_user = UserAccount.objects.filter(name=userto).first()
        validatedata_from_user = validated_data['from_user']
        userfrom = validatedata_from_user['username']
        from_user = UserAccount.objects.filter(name=userfrom).first()
        if not Relation.objects.filter(from_user=from_user,to_user=to_user) and from_user == log_in:
            return Relation.objects.create(from_user=from_user,to_user=to_user)
        raise ValidationError("you have followed before")

class FollowingListSerializer(serializers.ModelSerializer):
    to_user = serializers.CharField(source='to_user.username')
    image = serializers.ImageField(source='to_user.profile_picture')

    class Meta:
        model = Relation
        fields = ('to_user', 'image')

class FollowerListSerializer(serializers.ModelSerializer):
    from_user = serializers.CharField(source='from_user.username')
    image = serializers.ImageField(source='from_user.profile_picture')

    class Meta:
        model = Relation
        fields = ('from_user', 'image')
