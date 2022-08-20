from rest_framework import serializers
from content.models import  Post

from .models import Media

class PostMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ('id', 'media_file', 'media_type')

class PostListSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username')
    media = PostMediaSerializer(many=True)
    class Meta:
        model = Post
        # fields = '__all__'
        fields = ('id',  'caption', 'user', 'media')




class PostDetailSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username')
    class Meta:
        model = Post
        fields = ('id', 'caption', 'user')

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

