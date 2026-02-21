from django.urls import include, path

from .common.views import ApiRootView


urlpatterns = [
    path("", ApiRootView.as_view(), name="api-root"),
    path("auth/", include("api.user.urls")),
    path("content/", include("api.content.urls")),
]
