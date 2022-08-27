from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView,\
     RetrieveUpdateDestroyAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response


from .models import Comment, Like
from .serializers import CommentCreateSerializer, CommentListSerializer, CommentUpdateSerializer,\
    LikeCreateSerializer, LikeListSerializer
from account.models import UserAccount

from relation.permissions import RelationExists, HasPostPermission


class CommentCreateAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer

    def perform_create(self, serializer):
        user = self.request.user.id
        useraccount = UserAccount.objects.filter(username_id=user).first()
        serializer.save(user=useraccount)


class CommentListAPIView(ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentListSerializer
    permission_classes = (IsAuthenticated, )

class CommentRetrieveAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentListSerializer
    permission_classes = (IsAuthenticated, )

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return self.serializer_class
        return CommentUpdateSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user.id
        useraccount = UserAccount.objects.filter(username_id=user).first()
        return qs.filter(user=useraccount)
    
class DeleteCommentAPIView(DestroyAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = CommentListSerializer
    queryset = Comment.objects.all()
    
    def delete(self, request, pk, *args, **kwargs):
        comment = get_object_or_404(Comment, **{'pk': pk})
        log_in = UserAccount.objects.get(username=request.user)
        if comment.user == log_in:
            self.destroy(request, *args, **kwargs)
            content = {'message': 'deleted'}
            return Response(content,status=status.HTTP_200_OK)
        else:
            content = {'message': 'you cant delete'}
            return Response(content,status=status.HTTP_400_BAD_REQUEST)

class LikeCreateAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Like.objects.all()
    serializer_class = LikeCreateSerializer


    def perform_create(self, serializer):
        user = self.request.user.id
        useraccount = UserAccount.objects.filter(username_id=user).first()
        serializer.save(user=useraccount)

class LiketListAPIView(ListAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeListSerializer
    permission_classes = (IsAuthenticated, )

class DeleteLikeAPIView(DestroyAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = LikeListSerializer
    queryset = Like.objects.all()

    def delete(self, request, pk, *args, **kwargs):
        like = get_object_or_404(Like, **{'pk': pk})
        log_in = UserAccount.objects.get(username=request.user)
        if like.user == log_in:
            self.destroy(request, *args, **kwargs)
            content = {'message': 'deleted'}
            return Response(content,status=status.HTTP_200_OK)
        else:
            content = {'message': 'you cant delete'}
            return Response(content,status=status.HTTP_400_BAD_REQUEST)
