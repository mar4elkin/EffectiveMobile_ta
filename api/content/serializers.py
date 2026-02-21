from rest_framework import serializers

from mockapp.models import MockResource


class MockResourceSerializer(serializers.ModelSerializer):
    detail_url = serializers.HyperlinkedIdentityField(
        view_name="content-detail",
        lookup_field="pk",
    )

    class Meta:
        model = MockResource
        fields = ("id", "detail_url", "name", "data")
