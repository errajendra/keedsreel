from django.urls import path
from .import LoginMobileOTPAPIView


urlpatterns = [
    path("auth/login/mobile-otp/", LoginMobileOTPAPIView.as_view(), name="login-mobile-otp-api"),
]