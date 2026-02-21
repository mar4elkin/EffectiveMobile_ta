from rest_framework import generics, permissions, reverse, status
from rest_framework.response import Response


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
