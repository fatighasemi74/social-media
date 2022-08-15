from django.views import View
from rest_framework_simplejwt.tokens import RefreshToken





class GenerateToken(View):

    def get_access_and_refresh_token(user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def get_new_access_token(user):
        refresh = RefreshToken.for_user(user)
        return {
            'access': str(refresh.access_token),
        }