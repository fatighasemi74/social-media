from django.urls import URLPattern, path

from .views import CreateRelationAPIView

urlpatterns = [
    path('create/',CreateRelationAPIView.as_view(), name='create-relation'),
]