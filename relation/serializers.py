from rest_framework import serializers

from account.models import UserAccount
from .models import Relation

class CreateOrDeleteRelationSerializer(serializers.ModelSerializer):
    # to_user = serializers.CharField(source='to_user.username')
    # to_user = serializers.SerializerMethodField()
    # to_user = serializers.CharField(
    #     source="to_user.username", read_only=True)
    # to_user = serializers.SerializerMethodField("get_to_user")

    class Meta:
        model = Relation
        fields = ("to_user",)


class RelationListSerializer(serializers.ModelSerializer):

    from_user = serializers.CharField(source='from_user.username')
    to_user = serializers.CharField(source='to_user.username')


    class Meta:
        model = Relation
        fields = ('from_user', 'to_user')

class FollowingListSerializer(serializers.ModelSerializer):
    to_user = serializers.CharField(source='to_user.username')
    image = serializers.ImageField(source='to_user.profile_picture')

    class Meta:
        model = Relation
        fields = ('to_user', 'image')

class FollowerListSerializer(serializers.ModelSerializer):
    from_user = serializers.CharField(source='from_user.username')
    image = serializers.ImageField(source='from_user.profile_picture')

    class Meta:
        model = Relation
        fields = ('from_user', 'image')