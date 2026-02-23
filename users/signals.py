from django.db.models.signals import post_save
from django.dispatch import receiver

from access.models import Role, UserRole
from users.models import User


ADMIN_ROLE_CODE = "admin"
ADMIN_ROLE_NAME = "admin"
ADMIN_ROLE_LEVEL = 1
VIEWER_ROLE_CODE = "viewer"
VIEWER_ROLE_NAME = "viewer"
VIEWER_ROLE_LEVEL = 3


@receiver(post_save, sender=User)
def ensure_default_roles(sender, instance, created=False, raw=False, **kwargs):
    if raw:
        return

    if instance.is_superuser:
        role, _ = Role.objects.get_or_create(
            code=ADMIN_ROLE_CODE,
            defaults={
                "name": ADMIN_ROLE_NAME,
                "level": ADMIN_ROLE_LEVEL,
            },
        )

        changed_fields = []
        if role.name != ADMIN_ROLE_NAME:
            role.name = ADMIN_ROLE_NAME
            changed_fields.append("name")
        if role.level != ADMIN_ROLE_LEVEL:
            role.level = ADMIN_ROLE_LEVEL
            changed_fields.append("level")
        if changed_fields:
            role.save(update_fields=changed_fields)

        UserRole.objects.get_or_create(user=instance, role=role)
        return

    if not created:
        return

    role, _ = Role.objects.get_or_create(
        code=VIEWER_ROLE_CODE,
        defaults={
            "name": VIEWER_ROLE_NAME,
            "level": VIEWER_ROLE_LEVEL,
        },
    )

    changed_fields = []
    if role.name != VIEWER_ROLE_NAME:
        role.name = VIEWER_ROLE_NAME
        changed_fields.append("name")
    if role.level != VIEWER_ROLE_LEVEL:
        role.level = VIEWER_ROLE_LEVEL
        changed_fields.append("level")
    if changed_fields:
        role.save(update_fields=changed_fields)

    UserRole.objects.get_or_create(user=instance, role=role)
