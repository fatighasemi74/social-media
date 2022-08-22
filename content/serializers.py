from rest_framework import serializers


from content.models import  Post
from activity.serializers import CommentListSerializer

class PostListSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username')
    user_image = serializers.ImageField(source='user.profile_picture')
    # media = PostMediaSerializer(many=True)
    class Meta:
        model = Post
        # fields = '__all__'
        fields = ('id','title',  'caption', 'user', 'image', 'user_image')

class PostCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'title', 'caption', 'user', 'image')



class PostDetailSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username')
    user_image = serializers.ImageField(source='user.profile_picture')
    # media = PostMediaSerializer(many=True)
    comments = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ('id','title',  'caption', 'user', 'image', 'user_image', 'comments')

    def get_comments(self, obj):
        serializer = CommentListSerializer(obj.comments.filter(reply_to__isnull=True), many=True)
        return serializer.data

class EditPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id','caption')
    def update(self, instance, validated_data):
        if validated_data['caption']:
            instance.caption = validated_data['caption']
        instance.save()
        return instance

class DeletePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"

