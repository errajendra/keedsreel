from django.urls import path
from . import (
    RegisterMobileOTPAPIView,
    LoginMobileOTPAPIView,
    LoginGoogleAPIView,
    LoginFacebookAPIView,
    RegenerateAccessTokenAPIVIew,
    CheckMobileNumberExistAPIView,
    ProfileAPIView,
    UpdateProfilePictureAPIView,
    RemoveProfilePictureAPIView,
    ActiveStoryAPIView,
    ArchiveStoryAPIView,
    CreateStoryAPIView,
    DeleteStoryAPIView,
)


urlpatterns = [
    # auth api's endpoints
    path(
        "auth/register/mobile-otp/",
        RegisterMobileOTPAPIView.as_view(),
        name="register-mobile-otp-api",
    ),
    path(
        "auth/login/mobile-otp/",
        LoginMobileOTPAPIView.as_view(),
        name="login-mobile-otp-api",
    ),
    path(
        "auth/check/mobile-number/",
        CheckMobileNumberExistAPIView.as_view(),
        name="check-mobile-number-exist-api",
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
    # profile api's endpoints
    path("user/profile/", ProfileAPIView.as_view(), name="get-user-profile-api"),
    path(
        "user/update/profile-picture/",
        UpdateProfilePictureAPIView.as_view(),
        name="update-user-profile-picture-api",
    ),
    path(
        "user/remove/profile-picture/",
        RemoveProfilePictureAPIView.as_view(),
        name="remove-user-profile-picture-api",
    ),
    # post API's enpoints
    path("stories/active/", ActiveStoryAPIView.as_view(), name="active-stories-api"),
    path("stories/archive/", ArchiveStoryAPIView.as_view(), name="archive-stories-api"),
    path("stories/create/", CreateStoryAPIView.as_view(), name="create-stories-api"),
    path("stories/delete/", DeleteStoryAPIView.as_view(), name="delete-stories-api"),
]
