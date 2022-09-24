from django.urls import URLPattern, path, include
from rest_framework import routers


from content.views import PostCreateAPIView, PostListAPIView,\
    PostEditAPIView, DeletePosAPIView, PostViewSet

router = routers.SimpleRouter()
router.register('post', PostViewSet, basename='post')


urlpatterns = [
    path('', include(router.urls)),

    path('posts/',PostListAPIView.as_view(), name='posts-list'),
    path('post/create/',PostCreateAPIView.as_view(), name='post-create'),
    path('post/edit/<int:pk>/', PostEditAPIView.as_view(), name='post-edit'),
    path('post/delete/<int:pk>/', DeletePosAPIView.as_view(), name='post-edit'),
]