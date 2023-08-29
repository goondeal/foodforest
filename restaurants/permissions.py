from rest_framework import permissions


class RestaurantPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        # The following actions are exclusive to restaurant owners (or staff) from the admin panel.
        if view.action in {'update', 'partial_update', 'destroy'}:
            return False

        if view.action == 'create':
            return request.user.is_authenticated

        return True


    def has_object_permission(self, request, view, obj):
        if view.action in {'update', 'partial_update', 'destroy'}:
            return False

        if view.action == 'create':
            return request.user.is_authenticated

        if view.action == 'retrieve':
            if request.user.is_authenticated:
                # TODO: change blocked condition when implementing block feature
                blocked = False
                return not blocked
            return True

        return False
