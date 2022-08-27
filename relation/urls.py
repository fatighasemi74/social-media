from django.urls import URLPattern, path

from .views import CreateRelationAPIView, RelationListAPIView

urlpatterns = [
    path('create/',CreateRelationAPIView.as_view(), name='create-relation'),
    path('list/',RelationListAPIView.as_view(), name='create-list'),
]