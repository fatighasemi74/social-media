from django.contrib.auth.models import User
from rest_framework.permissions import BasePermission

from .models import Relation

class RelationExists(BasePermission):

    def has_permission(self, request, view):
        # print(view.args)
        user = User.objects.filter(username=view.kwargs['username']).first()
        if user:
            relation = Relation.objects.filter(from_user=request.user, to_user=user).exists() | request.user == user
            return relation
        return False

class HasPostPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        # middle = obj.user
        user = User.objects.filter(username=obj.user).first()
        if Relation.objects.filter(from_user=request.user, to_user=user).exists() or request.user == user:
            return True
        return False
