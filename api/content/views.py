from django.db.models import Max, Min
from rest_framework import exceptions, generics, permissions, reverse, status
from rest_framework.response import Response

from access.permissions import AccessResourcePermission
from access.utils import is_admin_user
from mockapp.models import MockResource

from .serializers import MockResourceAccessRoleUpdateSerializer, MockResourceSerializer


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

    def get_serializer_class(self):
        if self.request.method == "POST":
            return MockResourceAccessRoleUpdateSerializer
        return MockResourceSerializer

    def _update_access_roles(self, request, *args, **kwargs):
        if not is_admin_user(request.user):
            raise exceptions.PermissionDenied("Only admin role can update access roles.")
        if set(request.data.keys()) != {"access_role"}:
            raise exceptions.ValidationError(
                {"detail": "Only 'access_role' field can be updated for this endpoint."}
            )

        resource = self.get_object()
        serializer = MockResourceAccessRoleUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        resource.access_role.set(serializer.validated_data["access_role"])
        return Response(MockResourceSerializer(resource, context=self.get_serializer_context()).data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        return self._update_access_roles(request, *args, **kwargs)
