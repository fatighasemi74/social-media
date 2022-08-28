from django.contrib.auth.models import User
from rest_framework.permissions import BasePermission

from .models import Relation
from account.models import UserAccount
from content.models import Post

class RelationExists(BasePermission):
    '''
        permission for user post if rrelation exists
    '''
    def has_permission(self, request, view):
        user = UserAccount.objects.filter(name=view.kwargs['username']).first()
        useraccount = UserAccount.objects.filter(username=request.user).first()
        if user:
            return Relation.objects.filter(from_user=useraccount, to_user=user).exists() or user == useraccount
        return False


class HasPostPermission(BasePermission):
    '''
        permission for post detail if rrelation exists
    '''
    def has_object_permission(self, request, view, obj):
        to_user = obj.user
        user = request.user
        from_user = UserAccount.objects.filter(username=user).first()
        if Relation.objects.filter(from_user=from_user, to_user=to_user).exists() or from_user == to_user:
            return True
        return False
