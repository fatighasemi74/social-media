from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


from .views import UserCreateAPIView

urlpatterns = [
    path('create/', UserCreateAPIView.as_view(), name='account-create'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),
]