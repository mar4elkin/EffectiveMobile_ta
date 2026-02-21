from rest_framework import exceptions, permissions

from access.models import RoleAction


class AccessResourcePermission(permissions.BasePermission):
    ACTION_BY_METHOD = {
        "GET": "read",
        "HEAD": "read",
        "OPTIONS": "read",
        "POST": "create",
        "PUT": "update",
        "PATCH": "update",
        "DELETE": "delete",
    }

    def _action_code(self, request):
        return self.ACTION_BY_METHOD.get(request.method)

    def _user_role_ids(self, user):
        return user.user_roles.values_list("role_id", flat=True)

    def _has_action_permission(self, user, action_code):
        if user.is_superuser:
            return True
        if action_code is None:
            return False

        role_ids = self._user_role_ids(user)
        action_sets = RoleAction.objects.filter(role_id__in=role_ids).values_list("action_codes", flat=True)
        return any(action_code in (codes or []) for codes in action_sets)

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            raise exceptions.NotAuthenticated("Authentication credentials were not provided.")

        if self._has_action_permission(user, self._action_code(request)):
            return True

        raise exceptions.PermissionDenied("You do not have permission to perform this action.")

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_superuser:
            return True

        if not self._has_action_permission(user, self._action_code(request)):
            raise exceptions.PermissionDenied("You do not have permission to perform this action.")

        if hasattr(obj, "can_user_view") and obj.can_user_view(user):
            return True

        raise exceptions.PermissionDenied("You do not have access to this resource.")
