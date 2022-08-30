from django.urls import URLPattern, path

from content.views import PostCreateAPIView, PostListAPIView,\
    PostEditAPIView, DeletePosAPIView, UserPostReadOnlyViewSet

user_post_detail = UserPostReadOnlyViewSet.as_view({'get': 'retrieve'})
user_post_list = UserPostReadOnlyViewSet.as_view({'get': 'list'})

urlpatterns = [
    path('posts/',PostListAPIView.as_view(), name='posts-list'),
    path('post/create/',PostCreateAPIView.as_view(), name='post-create'),
    path('post/detail/<int:pk>/', user_post_detail, name='post-detail'),
    path('post/edit/<int:pk>/', PostEditAPIView.as_view(), name='post-edit'),
    path('post/delete/<int:pk>/', DeletePosAPIView.as_view(), name='post-edit'),
    path('post/user/<str:username>/', user_post_list, name='user-post-list'),
]