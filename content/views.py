from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from django.http import QueryDict

from content.permissions import IsOwnerOrReadOnly
from content.models import Post
from content.serializers import PostListSerializer, PostDetailSerializer,\
    PostCreateSerializer, EditPostSerializer, DeletePostSerializer

from account.models import UserAccount

from relation.permissions import RelationExists, HasPostPermission

class PostCreateAPIView(generics.CreateAPIView):

    serializer_class = PostCreateSerializer
    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        if isinstance(request.data, QueryDict):
            request.data._mutable = True
        user = self.request.user.id
        useraccount = UserAccount.objects.filter(username_id=user).first()
        request.data['user'] = useraccount.id
        return super().post(request, *args, **kwargs)


class PostListAPIView(generics.ListAPIView):
    queryset = Post.objects.all()

    serializer_class = PostListSerializer
    permission_classes = (IsAuthenticated, )






class PostDetailAPIView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated, )#HasPostPermission)
    serializer_class = PostDetailSerializer
    queryset = Post.objects.all()
    # def get(self, request, pk, *args, **kwargs):
    #     instance = get_object_or_404(Post, **{'pk':pk})
    #     serializer = PostDetailSerializer(instance)
    #     return Response(serializer.data)

    
class PostEditAPIView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = EditPostSerializer
    queryset = Post.objects.all()


    def put(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, **{'pk': pk})
        log_in = UserAccount.objects.get(username=request.user)
        print(post.user)
        print(log_in)
        if post.user == log_in:

            serializer = EditPostSerializer(post)
            # print(serializer.data)
            return self.update(request, *args, **kwargs)
        else:
            content = {'message': 'you are not the owner'}
            return Response(content,status=status.HTTP_400_BAD_REQUEST)

class DeletePosAPIView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = DeletePostSerializer
    queryset = Post.objects.all()

    def delete(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, **{'pk': pk})
        log_in = UserAccount.objects.get(username=request.user)
        if post.user == log_in:
            self.destroy(request, *args, **kwargs)
            content = {'message': 'deleted'}
            return Response(content,status=status.HTTP_200_OK)
        else:
            content = {'message': 'you cant delete'}
            return Response(content,status=status.HTTP_400_BAD_REQUEST)

class UserPostListAPIView(generics.ListAPIView):
    serializer_class = PostDetailSerializer
    permission_classes = (IsAuthenticated, )#RelationExists )
    queryset = Post.objects.all()
    lookup_url_kwarg = 'username'

    # pagination_class = PageNumberPagination
    # page_size = 10
    # pagination_class.page_size = page_size

    def get_queryset(self):
        qs = super().get_queryset()
        username = self.kwargs[self.lookup_url_kwarg]
        user = UserAccount.objects.filter(name=username).first()
        return qs.filter(user=user.id)


