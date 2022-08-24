from django.contrib.auth.models import User
from rest_framework.permissions import BasePermission

from .models import Relation

class RelationExists(BasePermission):

    def has_permission(self, request, view):
        user = User.objects.filter(username=view.kwargs['username']).first()
        if user:
            relation = Relation.objects.filter(from_user=request.user, to_user=user).exists()
            return relation
        return False
