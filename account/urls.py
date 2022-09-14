from django.urls import path, include
from rest_framework import routers



from .views import UserCreateAPIView, LogoutView, \
    LoginView, ProfileViewSet, RefreshTokenAPIView,\
    FollowingPostsAPIView, ExploreAPIView, VerificationView


router = routers.SimpleRouter()
router.register('profile', ProfileViewSet, basename='profile')

urlpatterns = [
    path('', include(router.urls)),

    path('create/', UserCreateAPIView.as_view(), name='account-create'),
    path('login/', LoginView.as_view(), name='login'),
    path('refresh-token/', RefreshTokenAPIView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('home/', FollowingPostsAPIView.as_view(), name='home'),
    path('explore/', ExploreAPIView.as_view(), name='home'),
    path('activate/<str:username>/', VerificationView.as_view(), name='activate'),

]