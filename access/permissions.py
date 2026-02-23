from rest_framework import exceptions, permissions

from access.utils import is_admin_user


class AccessResourcePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            raise exceptions.NotAuthenticated("Authentication credentials were not provided.")
        return True

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_superuser or is_admin_user(user):
            return True

        if hasattr(obj, "can_user_view") and obj.can_user_view(user):
            return True

        raise exceptions.PermissionDenied("You do not have access to this resource.")
