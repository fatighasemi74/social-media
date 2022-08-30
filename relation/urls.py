from django.urls import URLPattern, path

from .views import CreateRelationAPIView, RelationListAPIView, DeleteRelationAPIView,\
    FollowingAPIView, FollowerAPIView


urlpatterns = [
    path('create/',CreateRelationAPIView.as_view(), name='create-relation'),
    path('list/',RelationListAPIView.as_view(), name='list'),
    path('delete/<str:username>/',DeleteRelationAPIView.as_view(), name='delete-relation'),
    path('follower/<str:username>/', FollowerAPIView.as_view(), name='user-follower'),
    path('following/<str:username>/', FollowingAPIView.as_view(), name='user-following'),
]