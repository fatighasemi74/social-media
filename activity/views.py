from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView,\
     RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated



from .models import Comment
from .serializers import CommentCreateSerializer, CommentListSerializer, CommentUpdateSerializer
from account.models import UserAccount

class CommentCreateAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
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

