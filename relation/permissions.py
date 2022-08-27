from django.contrib.auth.models import User
from rest_framework.permissions import BasePermission

from .models import Relation
from account.models import UserAccount

class RelationExists(BasePermission):

    def has_permission(self, request, view):
        # print(view.args)
        user = UserAccount.objects.filter(username=view.kwargs['username']).first()
        if user:
            relation = Relation.objects.filter(from_user=request.user, to_user=user).exists() | request.user == user
            return relation
        return False

class HasPostPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        to_user = obj.user
        user = request.user
        from_user = UserAccount.objects.filter(username=user).first()
        if Relation.objects.filter(from_user=from_user, to_user=to_user).exists() or from_user == to_user:
            return True
        return False
