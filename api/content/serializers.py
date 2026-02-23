from rest_framework import serializers

from access.models import Role
from mockapp.models import MockResource


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ("id", "code", "name", "level")


class MockResourceSerializer(serializers.ModelSerializer):
    detail_url = serializers.HyperlinkedIdentityField(
        view_name="content-detail",
        lookup_field="pk",
    )
    access_role = RoleSerializer(many=True, read_only=True)

    class Meta:
        model = MockResource
        fields = ("id", "detail_url", "name", "data", "access_role")


class MockResourceAccessRoleUpdateSerializer(serializers.Serializer):
    access_role = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Role.objects.all(),
    )
