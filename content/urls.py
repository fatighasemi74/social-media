from django.urls import URLPattern, path

from content.views import PostCreateAPIView, PostListAPIView,\
    PostDetailAPIView, PostEditAPIView, DeletePosAPIView, UserPostListAPIView

urlpatterns = [
    path('posts/',PostListAPIView.as_view(), name='posts-list'),
    path('post/create/',PostCreateAPIView.as_view(), name='post-create'),
    path('post/detail/<int:pk>/', PostDetailAPIView.as_view(), name='post-detail'),
    path('post/edit/<int:pk>/', PostEditAPIView.as_view(), name='post-edit'),
    path('post/delete/<int:pk>/', DeletePosAPIView.as_view(), name='post-edit'),
    path('post/user/<int:user_id>/', UserPostListAPIView.as_view(), name='user-post-list')
]