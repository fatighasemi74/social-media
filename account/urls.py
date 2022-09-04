from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, \
    TokenRefreshView, TokenVerifyView


from .views import UserCreateAPIView, LogoutView, \
    LoginView, ProfileViewSet, EditProfileView,\
    ChangePasswordView, MyTokenObtainPairView, RefreshTokenAPIView,\
    DeleteUserAPIView, FollowingPostsAPIView

urlpatterns = [
    path('create/', UserCreateAPIView.as_view(), name='account-create'),
    # path('refresh/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('refresh/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/', LoginView.as_view(), name='token_obtain_pair'),
    path('refresh-token/', RefreshTokenAPIView.as_view(), name='token_refresh'),
    # path('verify-token/', TokenVerifyView.as_view(), name='token_verify'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/<str:username>/', ProfileViewSet.as_view({'get': 'get_queryset'}), name='profile'),
    path('edit_profile/<str:username>/', EditProfileView.as_view(), name='edit-profile'),
    path('change_password/<int:pk>/', ChangePasswordView.as_view(), name='change_password'),
    path('delete_account/<int:pk>/', DeleteUserAPIView.as_view(), name='delete_account'),
    path('home/', FollowingPostsAPIView.as_view(), name='home'),


]