from django.urls import path
from . import (
    LoginMobileOTPAPIView,
    LoginGoogleAPIView,
    LoginFacebookAPIView,
    RegenerateAccessTokenAPIVIew,
)


urlpatterns = [
    path(
        "auth/login/mobile-otp/",
        LoginMobileOTPAPIView.as_view(),
        name="login-mobile-otp-api",
    ),
    path("auth/login/google/", LoginGoogleAPIView.as_view(), name="login-google-api"),
    path(
        "auth/login/facebook/",
        LoginFacebookAPIView.as_view(),
        name="login-facebook-api",
    ),
    path(
        "auth/regenerate-access-token/",
        RegenerateAccessTokenAPIVIew.as_view(),
        name="regenerate-access-token-api",
    ),
]
