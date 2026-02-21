from django.contrib.auth import authenticate, login, logout
from django.db.models import Max, Min
from rest_framework import generics, permissions, reverse, serializers, status
from rest_framework.response import Response

from access.permissions import AccessResourcePermission
from mockapp.models import MockResource

from .serializers import (
    LoginSerializer,
    MockResourceSerializer,
    UserProfileSerializer,
    UserRegistrationSerializer,
)


class EmptySerializer(serializers.Serializer):
    pass


class ApiRootView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response(
            {
                "auth": reverse.reverse("auth-root", request=request),
                "content": reverse.reverse("content-root", request=request),
            },
            status=status.HTTP_200_OK,
        )


class AuthRootView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response(
            {
                "register": reverse.reverse("register", request=request),
                "login": reverse.reverse("login", request=request),
                "logout": reverse.reverse("logout", request=request),
                "profile": reverse.reverse("profile", request=request),
                "delete_account": reverse.reverse("delete-account", request=request),
            },
            status=status.HTTP_200_OK,
        )


class ContentRootView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        content_root_url = reverse.reverse("content-root", request=request)
        first_resource = MockResource.objects.order_by("pk").first()
        detail_example = None
        if first_resource:
            detail_example = reverse.reverse(
                "content-detail",
                args=[first_resource.pk],
                request=request,
            )
        return Response(
            {
                "list": reverse.reverse("content-list", request=request),
                "detail": f"{content_root_url}<pk>/",
            },
            status=status.HTTP_200_OK,
        )


class RegisterView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            UserProfileSerializer(user).data,
            status=status.HTTP_201_CREATED,
        )


class LoginView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        user = authenticate(request, username=email, password=password)
        if user is None:
            return Response(
                {"detail": "Invalid email or password."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        login(request, user)
        return Response(UserProfileSerializer(user).data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EmptySerializer

    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user


class DeleteAccountView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EmptySerializer

    def post(self, request):
        request.user.soft_delete()
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ContentListView(generics.ListAPIView):
    permission_classes = [AccessResourcePermission]
    serializer_class = MockResourceSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = MockResource.objects.all().prefetch_related("access_role")
        if user.is_superuser:
            return queryset

        user_min_level = user.user_roles.aggregate(min_level=Min("role__level"))["min_level"]
        if user_min_level is None:
            return queryset.none()

        return queryset.annotate(max_level=Max("access_role__level")).filter(max_level__gte=user_min_level)


class ContentDetailView(generics.RetrieveAPIView):
    permission_classes = [AccessResourcePermission]
    serializer_class = MockResourceSerializer
    queryset = MockResource.objects.all().prefetch_related("access_role")
