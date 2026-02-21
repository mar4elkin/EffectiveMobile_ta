from django.urls import path, re_path

from .views import (
    ApiRootView,
    AuthRootView,
    ContentDetailView,
    ContentListView,
    ContentRootView,
    DeleteAccountView,
    LoginView,
    LogoutView,
    ProfileView,
    RegisterView,
)


urlpatterns = [
    path("", ApiRootView.as_view(), name="api-root"),
    path("auth/", AuthRootView.as_view(), name="auth-root"),
    path("content/", ContentRootView.as_view(), name="content-root"),
    path("content/list/", ContentListView.as_view(), name="content-list"),
    path("content/<int:pk>/", ContentDetailView.as_view(), name="content-detail"),
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    path("auth/profile/", ProfileView.as_view(), name="profile"),
    path("auth/delete-account/", DeleteAccountView.as_view(), name="delete-account"),
]
