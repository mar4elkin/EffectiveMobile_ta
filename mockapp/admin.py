from django.contrib import admin
from django.db.models import Max, Min

from mockapp.models import MockResource


@admin.register(MockResource)
class MockResourceAdmin(admin.ModelAdmin):
    filter_horizontal = ("access_role",)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset

        user_min_level = request.user.user_roles.aggregate(min_level=Min("role__level"))["min_level"]
        if user_min_level is None:
            return queryset.none()

        return queryset.annotate(max_level=Max("access_role__level")).filter(max_level__gte=user_min_level)

    def has_module_permission(self, request):
        if request.user.is_superuser:
            return True
        return self.get_queryset(request).exists()

    def has_view_permission(self, request, obj=None):
        if obj is None:
            return self.has_module_permission(request)
        return obj.can_user_view(request.user)
