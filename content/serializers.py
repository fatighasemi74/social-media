from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from content.models import  Post, Comment, Like
from account.models import UserAccount
from account.serializers import  ProfileSerializer



class PostCreateSerializer(serializers.ModelSerializer):
    '''
        create post serializer
    '''
    username = serializers.CharField(source='user.username', read_only=True)
    user_image = serializers.ImageField(source='user.profile_picture', read_only=True)
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)

    # user = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), source='user.user')
    # user = ProfileSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'caption', 'user','username', 'user_image', 'image', 'created_time', 'comments_count', 'likes_count')
        extra_kwargs = {
        "caption": {
            "validators": [],
        },
    }

    def validate_caption(self, attr):
        '''
            validation method for caption length
        '''
        if attr == "":
            raise ValidationError({'message': 'کپشن خالی ست.', 'status': 400})
        return attr
    # def create(self, validated_data):
    #     # user = validated_data['user']
    #     print(validated_data, 'rrrrrr')
    #     # print(instance, 'inssss')
    #     # self.instance.user = validated_data['user']
    #     # instance.save()
    #
    #     return Post.objects.create(**validated_data)


class PostSerializer(serializers.ModelSerializer):
    '''
        post serializer for user post, post detail, edit post, delete post
    '''
    username = serializers.CharField(source='user.username')
    user_image = serializers.ImageField(source='user.profile_picture')
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)
    is_liked = serializers.SerializerMethodField()
    # comments = serializers.SerializerMethodField()
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    # media = PostMediaSerializer(many=True)
    class Meta:
        model = Post
        # fields = '__all__'
        fields = ('id','title',  'caption', 'username', 'image', 'user_image', 'comments_count', 'likes_count', 'created_time', 'is_liked')

    # def get_comments(self, obj):
    #     serializer = CommentListSerializer(obj.comments.filter(reply_to__isnull=True), many=True)
    #     return serializer.count()

    def get_is_liked(self, obj):
        request = self.context['request'].user
        log_in = UserAccount.objects.filter(name=request).first()
        # serializer = LikeSerializer(obj.likes.all(), many=True)
        likes = obj.likes.first()
        if obj.likes.first():
            if log_in == likes.user:
                return True
        return False
        # return serializer.data


class CommentCreateSerializer(serializers.ModelSerializer):
    '''
        create comment serializer
    '''
    username = serializers.CharField(source='user.username', read_only=True)
    user_image = serializers.ImageField(source='user.profile_picture', read_only=True)
    class Meta:
        model = Comment
        fields = ('id' ,'caption', 'post', 'reply_to', 'username', 'user_image')
        extra_kwargs = {
            'caption': {
                'validators': []
            }
        }


    def validate_caption(self, attr):
        '''
            validation method for caption length
        '''
        if attr == "":
            raise ValidationError({'message': 'کپشن خالی ست.', 'status': 400})
        elif len(attr) > 30:
            raise ValidationError({'message': 'کپشن طولانی ست.', 'status': 400})
        return attr

    def validate_post(self, attr):
        '''
            validation method for caption length
        '''
        if attr == "":
            raise ValidationError({'message': 'کپشن خالی ست.', 'status': 400})

        return attr

    def validators_reply_to(self, attr):
        '''
            validation method for reply
        '''
        if attr.reply_to is not None:
            raise ValidationError("you can not reply to a reply recursively")
        return attr



class CommentSerializer(serializers.ModelSerializer):
    '''
        comment serializer for list, comment detail, edit comment, delete comment
    '''
    username = serializers.CharField(source='user.username')
    user_image = serializers.ImageField(source='user.profile_picture')
    # replies = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ('id', 'caption', 'username', 'created_time', 'user_image')

    # def get_replies(self, obj):
    #     qs = obj.replies.all()
    #
    #     if qs.count() > 10:
    #         qs = qs[:10]
    #
    #     serializer = CommentRepliesListSerializer(qs, many=True)
    #     return serializer.data

class LikeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['post']

    def validate_post(self, attr):
        '''
            validation method for caption length
        '''
        if attr == "":
            raise ValidationError({'message': 'کپشن خالی ست.', 'status': 400})

        return attr

class LikeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    class Meta:
        model = Like
        fields = ('id', 'username', 'post')