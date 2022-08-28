from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status


from account.models import UserAccount
from .models import Relation
from .serializers import CreateOrDeleteRelationSerializer, RelationListSerializer, DeleteRelation

class CreateRelationAPIView(CreateAPIView):
    queryset = Relation.objects.all()
    serializer_class = CreateOrDeleteRelationSerializer
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

class DeleteRelationAPIView(DestroyAPIView):
    queryset = Relation.objects.all()
    serializer_class = DeleteRelation
    permission_classes = (IsAuthenticated, )
    lookup_url_kwarg = 'username'


    def delete(self, request, username, *args, **kwargs):
        useraccount = UserAccount.objects.filter(name=username).first()
        relation = Relation.objects.filter(to_user=useraccount.id).first()
        print(relation)
        if relation:
            # self.destroy(request, *args, **kwargs)
            relation.delete()
            content = {'message': 'deleted'}
            return Response(content,status=status.HTTP_200_OK)
        else:
            content = {'message': 'you cant delete'}
            return Response(content,status=status.HTTP_400_BAD_REQUEST)