from django.urls import path

from .views import (
    AuthRootView,
    DeleteAccountView,
    LoginView,
    LogoutView,
    ProfileView,
    RegisterView,
)


urlpatterns = [
    path("", AuthRootView.as_view(), name="auth-root"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("delete-account/", DeleteAccountView.as_view(), name="delete-account"),
]
