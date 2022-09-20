from django.urls import path, include
from rest_framework import routers



from .views import UserCreateAPIView, LogoutView, \
    LoginView, ProfileViewSet, RefreshTokenAPIView,\
     VerificationView, RelationViewSet, \
    FollowerAPIView, FollowingAPIView, ListPostViewSet


router = routers.SimpleRouter()
router.register('profile', ProfileViewSet, basename='profile')
router.register('relation', RelationViewSet, basename='relation')
router.register('list', ListPostViewSet, basename='list')

urlpatterns = [
    path('', include(router.urls)),

    path('create/', UserCreateAPIView.as_view(), name='account-create'),
    path('login/', LoginView.as_view(), name='login'),
    path('follower/<str:username>/', FollowerAPIView.as_view(), name='user-follower'),
    path('following/<str:username>/', FollowingAPIView.as_view(), name='user-following'),
    path('refresh-token/', RefreshTokenAPIView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('activate/<str:username>/', VerificationView.as_view(), name='activate'),

]