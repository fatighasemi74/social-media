from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Relation
from .serializers import CreateRelationSerializer
from .permissions import RelationExists, HasPostPermission

class CreateRelationAPIView(CreateAPIView):
    queryset = Relation.objects.all()
    serializer_class = CreateRelationSerializer
    permission_classes = [IsAuthenticated, HasPostPermission]

    def perform_create(self, serializer):
        # print(self.request.user)
        serializer.save(from_user=self.request.user)
