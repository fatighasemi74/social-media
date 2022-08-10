from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, \
    TokenRefreshView, TokenVerifyView


from .views import UserCreateAPIView, LogoutView, LoginView, ProfileViewSet

urlpatterns = [
    path('create/', UserCreateAPIView.as_view(), name='account-create'),
    # path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/', LoginView.as_view(), name='token_obtain_pair'),
    path('refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify-token/', TokenVerifyView.as_view(), name='token_verify'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/<int:pk>/', ProfileViewSet.as_view({'get': 'get_queryset'}), name='profile'),
]