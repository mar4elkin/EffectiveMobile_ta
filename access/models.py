from django.db import models
from effective_mobile_ta import settings

class Role(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    level = models.PositiveIntegerField(default=1, db_index=True)

    def __str__(self):
        return self.code


class Action(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.code


class RoleAction(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="permissions")
    actions = models.ManyToManyField(Action, related_name="role_permissions", blank=True)


class UserRole(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_roles")
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="user_roles")

    class Meta:
        unique_together = ("user", "role")

    def __str__(self):
        return f"{self.user_id}:{self.role.code}"
