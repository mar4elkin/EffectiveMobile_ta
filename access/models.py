from django.db import models
from django.core.exceptions import ValidationError
from effective_mobile_ta import settings


ACTION_CHOICES = (
    ("read", "Read"),
    ("create", "Create"),
    ("update", "Update"),
    ("delete", "Delete"),
)


class Role(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    level = models.PositiveIntegerField(default=1, db_index=True, unique=True)

    def __str__(self):
        return self.code


ALLOWED_ACTION_CODES = {code for code, _ in ACTION_CHOICES}


def validate_action_codes(value):
    if not isinstance(value, list):
        raise ValidationError("Action codes must be a list.")
    unknown_codes = [code for code in value if code not in ALLOWED_ACTION_CODES]
    if unknown_codes:
        raise ValidationError(f"Unknown action codes: {', '.join(sorted(set(unknown_codes)))}")


class RoleAction(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="permissions")
    action_codes = models.JSONField(default=list, blank=True, validators=[validate_action_codes])

    def __str__(self):
        return f"{self.role.code}:{','.join(self.action_codes)}"


class UserRole(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_roles")
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="user_roles")

    class Meta:
        unique_together = ("user", "role")

    def __str__(self):
        return f"{self.user} - {self.role.code}"
