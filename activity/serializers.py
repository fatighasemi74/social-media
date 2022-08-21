from rest_framework import serializers

from .models import Comment

class CommentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('caption', 'post', 'reply_to')