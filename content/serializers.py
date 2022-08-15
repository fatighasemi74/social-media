from rest_framework import serializers
from content.models import  Post


class PostListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = '__all__'

class PostDetailSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username')

    class Meta:
        model = Post
        fields = ('id', 'caption', 'user')

