from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from content.models import Post
from content.serializers import PostListSerializer


class PostCreateAPIView(generics.CreateAPIView):

    serializer_class = PostListSerializer
    # permission_classes = (IsAuthenticated, )



class PostListAPIView(generics.ListAPIView):
    queryset = Post.objects.all()

    serializer_class = PostListSerializer
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        user = request.user
        posts = user.Post.all()
        serializer = PostListSerializer(posts, many=True)
        # print(request)
        return Response(serializer.data)

