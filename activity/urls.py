from django.urls import URLPattern, path

from .views import CommentCreateAPIView, CommentListAPIView, \
    CommentRetrieveAPIView, LikeCreateAPIView

urlpatterns = [
    path('comment/create/',CommentCreateAPIView.as_view(), name='comment-create'),
    path('comments/',CommentListAPIView.as_view(), name='comment-list'),
    path('comment/retrieve/<int:pk>/',CommentRetrieveAPIView.as_view(), name='comment-retrieve'),
    path('like/create/', LikeCreateAPIView.as_view(), name='like-create'),

]