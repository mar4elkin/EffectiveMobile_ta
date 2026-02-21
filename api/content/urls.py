from django.urls import path

from .views import ContentDetailView, ContentListView, ContentRootView


urlpatterns = [
    path("", ContentRootView.as_view(), name="content-root"),
    path("list/", ContentListView.as_view(), name="content-list"),
    path("<int:pk>/", ContentDetailView.as_view(), name="content-detail"),
]
