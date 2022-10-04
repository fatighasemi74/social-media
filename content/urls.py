from django.urls import URLPattern, path, include
from rest_framework import routers


from content.views import PostCreateAPIView, PostViewSet, CommentCreateAPIView, \
    CommentViewSet, LikeCreateAPIView, LikeViewSet

router = routers.SimpleRouter()
router.register('post', PostViewSet, basename='post')
router.register('comment', CommentViewSet, basename='comment')
router.register('like', LikeViewSet, basename='like')


urlpatterns = [
    path('', include(router.urls)),
    path('create/post/',PostCreateAPIView.as_view(), name='post-create'),
    path('create/comment/',CommentCreateAPIView.as_view(), name='comment-create'),
    path('create/like/',LikeCreateAPIView.as_view(), name='like-create'),
]