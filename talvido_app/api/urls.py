from django.urls import path
from . import (
    RegisterMobileOTPAPIView,
    LoginMobileOTPAPIView,
    LoginGoogleAPIView,
    LoginFacebookAPIView,
    RegenerateAccessTokenAPIVIew,
    CheckMobileNumberExistAPIView
)


urlpatterns = [
    path("auth/register/mobile-otp/",
        RegisterMobileOTPAPIView.as_view(),
        name="register-mobile-otp-api"),
    path(
        "auth/login/mobile-otp/",
        LoginMobileOTPAPIView.as_view(),
        name="login-mobile-otp-api",
    ),
    path(
        "auth/check/mobile-number/",
        CheckMobileNumberExistAPIView.as_view(),
        name="check-mobile-number-exist-api"
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
