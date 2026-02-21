from django.contrib import admin
from django import forms

from access.models import ACTION_CHOICES, Role, RoleAction, UserRole


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "level")
    ordering = ("level", "code")


class RoleActionAdminForm(forms.ModelForm):
    action_codes = forms.MultipleChoiceField(choices=ACTION_CHOICES, required=False)

    class Meta:
        model = RoleAction
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["action_codes"].initial = self.instance.action_codes if self.instance.pk else []

    def clean_action_codes(self):
        return list(self.cleaned_data.get("action_codes") or [])


@admin.register(RoleAction)
class RoleActionAdmin(admin.ModelAdmin):
    form = RoleActionAdminForm
    list_display = ("role", "get_action_codes")

    @admin.display(description="actions")
    def get_action_codes(self, obj):
        return ", ".join(obj.action_codes)


admin.site.register(UserRole)
