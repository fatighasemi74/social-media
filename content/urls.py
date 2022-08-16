from django.urls import URLPattern, path

from content.views import PostCreateAPIView, PostListAPIView, PostDetailAPIView, AuthorPostListAPIView, PostEditAPIView

urlpatterns = [
    path('posts/',PostListAPIView.as_view(), name='posts-list'),
    path('authors_posts/<str:username>/',AuthorPostListAPIView.as_view(), name='authors_posts-list'),
    path('post/create/',PostCreateAPIView.as_view(), name='post-create'),
    # path('tag/<int:pk>/', TagDetailAPI.as_view(), name='tag-detail'),
    path('post/detail/<int:pk>/', PostDetailAPIView.as_view(), name='post-detail'),
    path('post/edit/<int:pk>/', PostEditAPIView.as_view(), name='post-edit')
]