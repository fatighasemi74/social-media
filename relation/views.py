from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated

from account.models import UserAccount
from .models import Relation
from .serializers import CreateRelationSerializer, RelationListSerializer
from .permissions import RelationExists, HasPostPermission

class CreateRelationAPIView(CreateAPIView):
    queryset = Relation.objects.all()
    serializer_class = CreateRelationSerializer
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        user = self.request.user.id
        useraccount = UserAccount.objects.filter(username_id=user).first()
        serializer.save(from_user=useraccount)

class RelationListAPIView(ListAPIView):
    queryset = Relation.objects.all()

    serializer_class = RelationListSerializer
    permission_classes = (IsAuthenticated, )

    # def get_queryset(self):