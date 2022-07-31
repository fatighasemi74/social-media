from django.urls import URLPattern, path

from content.views import PostCreateAPIView, PostListAPIView

urlpatterns = [
    path('posts/',PostListAPIView.as_view(), name='posts-list'),
    path('post/create/',PostCreateAPIView.as_view(), name='post-create'),
    # path('tag/<int:pk>/', TagDetailAPI.as_view(), name='tag-detail'),
    # path('post/<int:pk>/', PostDetailAPI.as_view(), name='post-detail')
]
