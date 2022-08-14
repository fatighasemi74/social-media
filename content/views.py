from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404



from content.permissions import IsOwnerOrReadOnly
from content.models import Post
from content.serializers import PostListSerializer, PostDetailSerializer


class PostCreateAPIView(generics.CreateAPIView):

    serializer_class = PostListSerializer
    permission_classes = (IsAuthenticated, )



class PostListAPIView(generics.ListAPIView):
    queryset = Post.objects.all()

    serializer_class = PostListSerializer
    permission_classes = (IsAuthenticated, )

class AuthorPostListAPIView(generics.ListAPIView):
    serializer_class = PostListSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(name__startswith=self.kwargs['name'])


class PostDetailAPIView(APIView):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly )

    def get(self, request, pk, *args, **kwargs):
        instance = get_object_or_404(Post, **{'pk':pk})
        serializer = PostDetailSerializer(instance)
        return Response(serializer.data)
    
class PostEditAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly, )







