from rest_framework import serializers

from account.models import UserAccount
from .models import Relation

class CreateRelationSerializer(serializers.ModelSerializer):
    # to_user = serializers.CharField(source='to_user.username')
    # to_user = serializers.SerializerMethodField()
    # to_user = serializers.CharField(
    #     source="to_user.username", read_only=True)
    # to_user = serializers.SerializerMethodField("get_to_user")

    class Meta:
        model = Relation
        fields = ("to_user",)

    # def validate
    # def get_to_user(self, obj):
    #     user_id = self.request.user.id
    #     # to_user = UserAccount.objects.filter(user=obj.to_user).first()
    #     print(self.obj)
    #     return user_id


class RelationListSerializer(serializers.ModelSerializer):

    from_user = serializers.CharField(source='from_user.username')
    to_user = serializers.CharField(source='to_user.username')

    class Meta:
        model = Relation
        fields = ('from_user', 'to_user')