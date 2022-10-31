from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import pagination
from django.http import QueryDict

from content.models import Post, Comment, Like
from content.serializers import PostSerializer, PostCreateSerializer,\
    CommentCreateSerializer, CommentSerializer, LikeCreateSerializer, \
    LikeSerializer
from account.models import UserAccount




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


class PostViewSet(viewsets.ModelViewSet):
    '''
        this viewset works for list of user posts, post detail, edit post and for deleting post
    '''
    serializer_class = PostSerializer
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
            serializer = PostSerializer(instance, context={'request': request})
            return Response(serializer.data)
        else:
            content = {'message': 'اجازه ی ادیت کردن ندارید.', 'status': 403}
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
            content = {"message": 'پاک شد.', 'status': 200}
            return Response(content,status=status.HTTP_200_OK)
        else:
            content = {"message": "اجازه ی پاک کردن ندارید.", 'status': 403}
            return Response(content, status=status.HTTP_403_FORBIDDEN)

class CommentCreateAPIView(generics.CreateAPIView):
    '''
        create new comment
    '''
    permission_classes = (IsAuthenticated, )
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer

    def perform_create(self, serializer):
        user = self.request.user.id
        useraccount = UserAccount.objects.filter(username_id=user).first()
        serializer.save(user=useraccount)



class CommentViewSet(viewsets.ModelViewSet):
    '''
        this viewset works for list of comments, comment detail, edit comment and for deleting comment
    '''
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated, )
    queryset = Comment.objects.all()
    pagination_class = Pagination
    lookup_field = 'pk'

    def get_queryset(self, *args, **kwargs):
        '''
            list of post comments, comment detail
        '''
        qs = super().get_queryset()
        param = self.request.GET.get('route')
        if param:
            post = Post.objects.filter(id=param).first()
            queryset = Comment.objects.filter(post=post.id)
            print(queryset)
            return queryset
        else:
            return qs


    def update(self, request, *args, **kwargs):
        '''
            edit comment
        '''
        log_in = UserAccount.objects.get(name=self.request.user)
        comment = Comment.objects.filter(id=kwargs['pk']).first()
        if comment.user == log_in:
            instance = self.get_object()
            if request.data.get('caption'):
                instance.caption = request.data.get('caption')
                instance.save()
            serializer = CommentSerializer(instance)
            return Response(serializer.data)
        else:
            content = {'message': 'اجازه ی ادیت کردن ندارید.', 'status': 403}
            return Response(content,status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, pk, *args, **kwargs):
        '''
            delete comment
        '''
        comment = Comment.objects.filter(id=self.kwargs['pk']).first()
        if comment:
            log_in = UserAccount.objects.get(username=request.user)
            if comment.user == log_in:
                comment.delete()
                content = {'message': 'پاک شد.'}
                return Response(content,status=status.HTTP_200_OK)
            else:
                content = {'message': 'اجازه ی پاک کردن ندارید.'}
                return Response(content,status=status.HTTP_400_BAD_REQUEST)
        else:
            content = {'message': 'همچین کامنتی وجود ندارد.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

class LikeCreateAPIView(generics.CreateAPIView):
    '''
        create like
    '''
    permission_classes = (IsAuthenticated, )
    queryset = Like.objects.all()
    serializer_class = LikeCreateSerializer


    def perform_create(self, serializer):
        user = self.request.user.id
        useraccount = UserAccount.objects.filter(username_id=user).first()
        serializer.save(user=useraccount)
        return serializer.data

class LikeViewSet(viewsets.ModelViewSet):
    '''
        this viewset works for list of likes and for deleting comment
    '''
    serializer_class = LikeSerializer
    permission_classes = (IsAuthenticated, )
    queryset = Like.objects.all()
    pagination_class = Pagination
    lookup_field = 'pk'

    def get_queryset(self, *args, **kwargs):
        '''
            list of post likes
        '''
        qs = super().get_queryset()
        param = self.request.GET.get('route')
        if param:
            post = Post.objects.filter(id=param).first()
            queryset = Like.objects.filter(post=post.id)
            return queryset
        else:
            return qs

    def destroy(self, request, pk, *args, **kwargs):
        '''
            delete like
        '''
        post = Post.objects.filter(id=self.kwargs['pk']).first()
        print(post.id, "jhhhhh")
        log_in = UserAccount.objects.get(username=request.user)

        like = Like.objects.filter(user=log_in, post=post).first()

        if like:
            like.delete()
            content = {'message': 'آنلایک شد.', 'status': 200}
            return Response(content,status=status.HTTP_200_OK)
        else:
            content = {'message': 'همچین لایکی وجود ندارد.', 'status': 400}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)



        # like = Like.objects.filter(id=self.kwargs['pk']).first()
        # if like:
        #     log_in = UserAccount.objects.get(username=request.user)
        #     if like.user == log_in:
        #         like.delete()
        #         content = {'message': 'آنلایک شد.'}
        #         return Response(content,status=status.HTTP_200_OK)
        #     else:
        #         content = {'message': 'اجازه ی آنلایک کردن ندارید.'}
        #         return Response(content,status=status.HTTP_400_BAD_REQUEST)
        # else:
        #     content = {'message': 'همچین لایکی وجود ندارد.'}
        #     return Response(content, status=status.HTTP_400_BAD_REQUEST)