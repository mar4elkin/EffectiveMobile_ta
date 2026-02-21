from django.db.models import Max, Min
from rest_framework import generics, permissions, reverse, status
from rest_framework.response import Response

from access.permissions import AccessResourcePermission
from mockapp.models import MockResource

from .serializers import MockResourceSerializer


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
