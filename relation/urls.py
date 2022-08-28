from django.urls import URLPattern, path

from .views import CreateRelationAPIView, RelationListAPIView, DeleteRelationAPIView

urlpatterns = [
    path('create/',CreateRelationAPIView.as_view(), name='create-relation'),
    path('list/',RelationListAPIView.as_view(), name='list'),
    path('delete/<str:username>/',DeleteRelationAPIView.as_view(), name='delete-relation'),
]