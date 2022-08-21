from rest_framework import serializers
from content.models import  Post


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
    class Meta:
        model = Post
        fields = ('id','title',  'caption', 'user', 'image', 'user_image')

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

