from django.urls import URLPattern, path

from .views import CommentCreateAPIView

urlpatterns = [
    path('comment/create/',CommentCreateAPIView.as_view(), name='comment-create'),
]