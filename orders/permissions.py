from django.shortcuts import get_object_or_404
from rest_framework import permissions
from restaurants.models import Restaurant


class CanOrder(permissions.BasePermission):
    """
    Global permission check for blocked users.
    """
    def has_permission(self, request, view):
        """
        Assert user is not blocked by the restaurant,
        and no open dispute between them.
        """
        r = get_object_or_404(Restaurant, slug=request.data.get('restaurant', ''))
        user_is_blocked = r.blocked_users.filter(id=request.user.id).exists()
        # TODO: assert that no disputes is open for that user
        return not user_is_blocked
