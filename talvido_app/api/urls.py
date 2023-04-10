from django.urls import path
from .import (
    LoginMobileOTPAPIView,
    LoginGoogleAPIView
)


urlpatterns = [
    path("auth/login/mobile-otp/", LoginMobileOTPAPIView.as_view(), name="login-mobile-otp-api"),
    path("auth/login/google/", LoginGoogleAPIView.as_view(), name="login-google-api"),
]
