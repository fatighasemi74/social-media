from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import viewsets



from content.permissions import IsOwnerOrReadOnly
from content.models import Post
from content.serializers import PostListSerializer, PostDetailSerializer, EditPostSerializer

from account.models import UserAccount


class PostCreateAPIView(generics.CreateAPIView):

    serializer_class = PostListSerializer
    permission_classes = (IsAuthenticated, )



class PostListAPIView(generics.ListAPIView):
    queryset = Post.objects.all()

    serializer_class = PostListSerializer
    permission_classes = (IsAuthenticated, )


class AuthorPostListAPIView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        username = self.kwargs['username']
        print('hiiiiiiiiiiiiiiii' , username)

        user = UserAccount.objects.filter(name=username).first()
        # print(user.id)
        posts = Post.objects.filter(user=user.id)
        print(posts)
        postSerializer = PostListSerializer(posts, many=True)
        print(postSerializer)
        if postSerializer.is_valid():
            postSerializer.save()
        print(postSerializer.data)
        return postSerializer.data




class PostDetailAPIView(APIView):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly )

    def get(self, request, pk, *args, **kwargs):
        instance = get_object_or_404(Post, **{'pk':pk})
        serializer = PostDetailSerializer(instance)
        return Response(serializer.data)

    
class PostEditAPIView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = EditPostSerializer
    queryset = Post.objects.all()


    def put(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, **{'pk': pk})
        serializer = EditPostSerializer(post)
        print(serializer.data)
        return self.update(request, *args, **kwargs)
