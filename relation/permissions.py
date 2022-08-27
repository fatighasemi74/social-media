from django.contrib.auth.models import User
from rest_framework.permissions import BasePermission

from .models import Relation
from account.models import UserAccount
from content.models import Post

class RelationExists(BasePermission):

    def has_permission(self, request, view):
        post = Post.objects.filter(id=view.kwargs['pk']).first()
        user = User.objects.filter(username=post.user).first()
        useraccount = UserAccount.objects.filter(username=user).first()
        from_user = UserAccount.objects.filter(username=request.user).first()
        if user:
            relation = Relation.objects.filter(from_user=from_user, to_user=useraccount).exists() or from_user == post.user
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
