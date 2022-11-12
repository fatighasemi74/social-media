from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User



from .models import UserAccount, Relation, Data



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

    def validate_name(self, attr):
        '''
            validation method for username
        '''
        if attr == "":
            raise ValidationError({'message': 'نام کاربری خالی ست.', 'status': 400})
        return attr

    def validate_email(self, attr):
        if attr == "":
            raise ValidationError({'message': 'ایمیل خالی ست.', 'status': 400})
        elif User.objects.filter(email=attr).exists():
            raise ValidationError({'message': 'ایمیل وجود ندارد.', 'status': 400})
        return attr
    # def clean(self):
    #     email = self.cleaned_data.get('email')
    #     if User.objects.filter(email=email).exists():
    #         raise ValidationError({'message': 'ایمیل وجود ندارد.', 'status': 400})
    #     return self.cleaned_data

    def validate(self, attr):
        if attr['password'] != attr['password2']:
            raise ValidationError({'message': "پسورد مطابقت ندارد.", 'status': 400})
        if len(attr['password']) < 7:
            raise ValidationError({'message' : "پسورد باید حداقل ۷ کاراکتر داشته باشد.", 'status': 400})
        return attr






    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(username=validated_data['name'])
        user.set_password(password)
        user.save()
        useraccount = UserAccount.objects.create(
                                                 name=validated_data['name'],
                                                 email=validated_data['email'],)
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
    posts_count = serializers.IntegerField(source='posts.count', read_only=True)
    is_followed = serializers.SerializerMethodField()
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
                  'old_password', 'password', 'password2', 'is_followed', 'posts_count')

    def get_date_joined(self, obj):
        date_joined = obj.username.date_joined
        return date_joined.strftime('%Y-%m-%d')


    def get_is_followed(self, obj):
        request = self.context['request'].user
        log_in = UserAccount.objects.filter(name=request).first()
        relations = obj.follewrs.first()
        if relations:
            if log_in == relations.from_user:
                return True
            return False
        return False

    # def get_follower(self, obj):
    #     serializer = RelationListSerializer(obj.follewrs.all(), many=True)
    #     return serializer.data[0]['from_user']

    # def get_following(self, obj):
    #     serializer = RelationListSerializer(obj.followings.all(), many=True)
    #     # print(serializer.data[0]['to_user'])
    #     return serializer.data[0]['to_user']

class ChangePasswordSerializer(serializers.ModelSerializer):
    """
    Serializer for password change endpoint.
    """
    password = serializers.CharField(write_only=True, required=True,
        style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True,
                                      style={'input_type': 'password'})
    old_password = serializers.CharField(write_only=True, required=True,
                                         style={'input_type': 'password'})

    class Meta:
        model = UserAccount
        fields = ('old_password', 'password', 'password2')



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
        if not Relation.objects.filter(from_user=from_user,to_user=to_user):
            if from_user == log_in:
                return Relation.objects.create(from_user=from_user,to_user=to_user)
            raise ValidationError({"message":"نمیتوانید!"})
        raise ValidationError({"message":"قبلا فالو کرده بودید."})

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

class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data
        fields = ('id', 'media_file', 'media_type', 'content_id')
