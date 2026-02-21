from django.db import models
from effective_mobile_ta import settings


class Role(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.code


class Resource(models.Model):
    code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.code


class Action(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.code


class RolePermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="permissions")
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name="permissions")
    action = models.ForeignKey(Action, on_delete=models.CASCADE, related_name="permissions")
    is_allowed = models.BooleanField(default=True)

    class Meta:
        unique_together = ("role", "resource", "action")

    def __str__(self):
        return f"{self.role.code}:{self.resource.code}:{self.action.code}={self.is_allowed}"


class UserRole(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_roles")
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="user_roles")

    class Meta:
        unique_together = ("user", "role")

    def __str__(self):
        return f"{self.user_id}:{self.role.code}"
