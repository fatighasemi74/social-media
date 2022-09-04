from rest_framework import serializers


from content.models import  Post
from activity.serializers import CommentListSerializer, LikeListSerializer

class PostListSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username')
    user_image = serializers.ImageField(source='user.profile_picture')
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)
    likes = serializers.SerializerMethodField()
    # likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    # media = PostMediaSerializer(many=True)
    class Meta:
        model = Post
        # fields = '__all__'
        fields = ('id','title',  'caption', 'user', 'image', 'user_image', 'comments_count', 'likes', 'created_time')

    # def get_comments(self, obj):
    #     serializer = CommentListSerializer(obj.comments.filter(reply_to__isnull=True), many=True)
    #     return serializer.count()
    def get_likes(self, obj):
        serializer = LikeListSerializer(obj.likes.all(), many=True)
        return serializer.data

class PostCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'title', 'caption', 'user', 'image', 'created_time')



class PostDetailSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username')
    user_image = serializers.ImageField(source='user.profile_picture')
    # media = PostMediaSerializer(many=True)
    comments = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()


    class Meta:
        model = Post
        fields = ('id','title',  'caption', 'user', 'image', 'user_image', 'comments', 'likes', 'created_time')

    def get_comments(self, obj):
        serializer = CommentListSerializer(obj.comments.filter(reply_to__isnull=True), many=True)
        return serializer.data

    def get_likes(self, obj):
        serializer = LikeListSerializer(obj.likes.all(), many=True)
        return serializer.data

class EditPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id','caption', 'title', 'image')
    def update(self, instance, validated_data):
        if validated_data['caption']:
            instance.caption = validated_data['caption']
        if validated_data['title']:
            instance.title = validated_data['title']
        if validated_data['image']:
            instance.image = validated_data['image']
        instance.save()
        return instance

class DeletePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"

