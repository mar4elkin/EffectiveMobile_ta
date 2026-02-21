from django.db import models
from django.db.models import Max
from access.models import Role


class MockResource(models.Model):
    name = models.CharField(max_length=100)
    data = models.TextField()

    access_role = models.ManyToManyField(Role, blank=True)

    def required_level(self):
        return self.access_role.aggregate(max_level=Max("level"))["max_level"]

    def can_user_view(self, user):
        if not user.is_authenticated:
            return False
        if user.is_superuser:
            return True

        required_level = self.required_level()
        if required_level is None:
            return False

        return user.user_roles.filter(role__level__lte=required_level).exists()

    def __str__(self):
        return self.name
