from django.contrib.auth import authenticate, login, logout
from rest_framework import generics, permissions, reverse, status
from rest_framework.response import Response

from .serializers import (
    EmptySerializer,
    LoginSerializer,
    UserProfileSerializer,
    UserRegistrationSerializer,
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
