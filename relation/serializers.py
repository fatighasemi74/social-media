from rest_framework import serializers
from .models import Relation

class CreateRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relation
        fields = ("to_user",)