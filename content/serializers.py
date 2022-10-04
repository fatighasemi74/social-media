from rest_framework import serializers
from rest_framework.exceptions import ValidationError


from content.models import  Post, Comment, Like



class PostCreateSerializer(serializers.ModelSerializer):
    '''
        create post serializer
    '''

    class Meta:
        model = Post
        fields = ('id', 'title', 'caption', 'user', 'image', 'created_time')


class PostSerializer(serializers.ModelSerializer):
    '''
        post serializer for user post, post detail, edit post, delete post
    '''
    user = serializers.CharField(source='user.username')
    user_image = serializers.ImageField(source='user.profile_picture')
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)
    # likes = serializers.SerializerMethodField()
    # comments = serializers.SerializerMethodField()
    # likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    # media = PostMediaSerializer(many=True)
    class Meta:
        model = Post
        # fields = '__all__'
        fields = ('id','title',  'caption', 'user', 'image', 'user_image', 'comments_count', 'created_time')

    # def get_comments(self, obj):
    #     serializer = CommentListSerializer(obj.comments.filter(reply_to__isnull=True), many=True)
    #     return serializer.count()
    # def get_likes(self, obj):
    #     serializer = LikeSerializer(obj.likes.all(), many=True)
    #     return serializer.data

class CommentCreateSerializer(serializers.ModelSerializer):
    '''
        create comment serializer
    '''
    class Meta:
        model = Comment
        fields = ('caption', 'post', 'reply_to')


    def validate_caption(self, attr):
        '''
            validation method for caption length
        '''
        if len(attr) > 30:
            raise ValidationError("Caption cannot be more than 30 characters!!")
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
    user = serializers.CharField(source='user.username')
    user_image = serializers.ImageField(source='user.profile_picture')
    # replies = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ('id', 'caption', 'user', 'created_time', 'user_image')

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

class LikeSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username')
    class Meta:
        model = Like
        fields = ('id', 'user')