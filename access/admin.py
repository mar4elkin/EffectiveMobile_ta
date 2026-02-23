from django.contrib import admin

from access.models import Role, UserRole


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "level")
    ordering = ("level", "code")


admin.site.register(UserRole)
