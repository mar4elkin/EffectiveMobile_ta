from django.contrib import admin

from access.models import Role, Action, RoleAction, UserRole


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "level")
    ordering = ("level", "code")


admin.site.register(Action)
admin.site.register(RoleAction)
admin.site.register(UserRole)
