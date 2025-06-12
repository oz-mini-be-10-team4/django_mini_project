from django.urls import path

from .views import LoginView, LogoutView, MeView, SignupView, TokenRefreshViewOverride

app_name = "user"

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("token/refresh/", TokenRefreshViewOverride.as_view(), name="token_refresh"),
    path("me/", MeView.as_view(), name="me"),
]
