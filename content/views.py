from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import pagination

from django.http import QueryDict

from content.permissions import IsOwnerOrReadOnly
from content.models import Post
from content.serializers import PostListSerializer, PostDetailSerializer,\
    PostCreateSerializer, EditPostSerializer, DeletePostSerializer

from account.models import UserAccount

from relation.permissions import RelationExists, HasPostPermission


class Pagination(pagination.PageNumberPagination):
    page_size = 2

class PostCreateAPIView(generics.CreateAPIView):
    '''
        create new post
    '''

    serializer_class = PostCreateSerializer
    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        if isinstance(request.data, QueryDict):
            request.data._mutable = True
        user = self.request.user.id
        useraccount = UserAccount.objects.filter(username_id=user).first()
        request.data['user'] = useraccount.id
        return super().post(request, *args, **kwargs)


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



class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostListSerializer
    permission_classes = (IsAuthenticated, )
    queryset = Post.objects.all()
    pagination_class = Pagination



    def get_queryset(self, *args, **kwargs):
        '''
            list of user posts, post detail
        '''
        qs = super().get_queryset()
        param = self.request.GET.get('route')
        if param:
            user = UserAccount.objects.filter(name=param).first()
            queryset = Post.objects.filter(user=user.id)
            print(queryset)
            return queryset
        else:
            return qs

    def update(self, request, *args, **kwargs):
        '''
            edit post
        '''
        log_in = UserAccount.objects.get(name=self.request.user)
        post = Post.objects.filter(id=kwargs['pk']).first()
        if post.user == log_in:
            instance = self.get_object()
            if request.data.get('caption'):
                instance.caption = request.data.get('caption')
                instance.save()
            if request.data.get('title'):
                instance.title = request.data.get('title')
                instance.save()
            if request.data.get('image'):
                instance.image = request.data.get('image')
                instance.save()
            serializer = PostListSerializer(instance)
            return Response(serializer.data)
        else:
            content = {'message': 'you cant edit this post.'}
            return Response(content,status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        '''
            delete post
        '''
        log_in = UserAccount.objects.get(name=self.request.user)
        post = Post.objects.filter(id=kwargs['pk']).first()
        print(post.user.id)
        if post.user == log_in:
            post.delete()
            content = {"message": 'delete'}
            return Response(content,status=status.HTTP_200_OK)
        else:
            content = {"message": "you cant delete"}
            return Response(content, status=status.HTTP_403_FORBIDDEN)



