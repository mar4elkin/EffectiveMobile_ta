from django.contrib.auth import get_user_model
from rest_framework import serializers

from access.models import UserRole
from mockapp.models import MockResource


User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "middle_name",
            "password",
            "password_confirm",
        )

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError(
                {"password_confirm": "Passwords do not match."}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop("password_confirm")
        password = validated_data.pop("password")
        return User.objects.create_user(password=password, **validated_data)


class UserProfileSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "middle_name", "role")

    def get_role(self, obj):
        user_role = (
            UserRole.objects.select_related("role")
            .filter(user=obj)
            .order_by("role__level", "id")
            .first()
        )
        if not user_role:
            return None

        role = user_role.role
        return {
            "code": role.code,
            "name": role.name,
            "level": role.level,
        }


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class MockResourceSerializer(serializers.ModelSerializer):
    detail_url = serializers.HyperlinkedIdentityField(
        view_name="content-detail",
        lookup_field="pk",
    )

    class Meta:
        model = MockResource
        fields = ("id", "detail_url", "name", "data")
