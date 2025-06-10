from django.urls import path
from .views import SignupView, LoginView, MeView, TokenRefreshViewOverride

app_name = "user"

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshViewOverride.as_view(), name="token_refresh"),
    path("me/", MeView.as_view(), name="me"),
]
