from rest_framework import serializers
from content.models import  Post


class PostListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = '__all__'

class PostDetailSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username')
    # comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'caption', 'user')

    # def get_comments(self, obj):
    #     serializer = CommentListSerializer(obj.comments.filter(reply_to_isnull=True), many=True)
    #     return serializer.data