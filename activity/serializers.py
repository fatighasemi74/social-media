from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Comment
# from content.serializers import PostDetailSerializer


class CommentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('caption', 'post', 'reply_to')

    def validate_caption(self, attr):
        if len(attr) > 30:
            raise ValidationError("Caption cannot be more than 30 characters!!")
        return attr
    def validators_reply_to(self, attr):
        if attr.reply_to is not None:
            raise ValidationError("you can not reply to a reply recursively")
        return attr


class CommentRepliesListSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username')

    class Meta:
        model = Comment
        fields = ('id', 'caption', 'user', 'reply_to')


class CommentListSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username')
    replies = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ('id', 'caption', 'user', 'replies')

    def get_replies(self, obj):
        qs = obj.replies.all()

        if qs.count() > 10:
            qs = qs[:10]

        serializer = CommentRepliesListSerializer(qs, many=True)
        return serializer.data

class CommentUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['caption']

    def validate_caption(self, attr):
        if len(attr) > 30:
            raise ValidationError("Caption cannot be more than 30 characters!!")
        return attr

