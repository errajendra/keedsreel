from django.urls import path
from . import (
    RegisterMobileOTPAPIView,
    LoginMobileOTPAPIView,
    LoginGoogleAPIView,
    LoginFacebookAPIView,
    RegsiterEmailAPIView,
    LoginEmailAPIView,
    RegenerateAccessTokenAPIVIew,
    CheckMobileNumberExistAPIView,
    ProfileAPIView,
    UpdateProfilePictureAPIView,
    RemoveProfilePictureAPIView,
    FollowersAPIView,
    FollowingsAPIView,
    GetAnyUserProfileAPIView,
    ActiveStoryAPIView,
    ArchiveStoryAPIView,
    CreateStoryAPIView,
    DeleteStoryAPIView,
    StoryViewAPIView,
    GetUserFollowingStories,
    GetAuthUserActivePosts,
    UploadPostAPIView,
    DeletePostAPIView,
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
        "auth/register/email/",
        RegsiterEmailAPIView.as_view(),
        name="register-email-api",
    ),
     path(
        "auth/login/email/",
        LoginEmailAPIView.as_view(),
        name="login-email-api",
    ),
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
    path("user/profile/", ProfileAPIView.as_view(), name="get-current-user-profile-api"),
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
    path("user/profile/followers/",FollowersAPIView.as_view(),name="user-followers-api"),
    path("user/profile/followings/",FollowingsAPIView.as_view(),name="user-followings-api"),
    path("user/profile/<str:firebase_uid>/",GetAnyUserProfileAPIView.as_view(),name="get-any-user-profile-api"),
    # post API's enpoints
    path("stories/active/", ActiveStoryAPIView.as_view(), name="active-stories-api"),
    path("stories/archive/", ArchiveStoryAPIView.as_view(), name="archive-stories-api"),
    path("stories/create/", CreateStoryAPIView.as_view(), name="create-stories-api"),
    path("stories/delete/", DeleteStoryAPIView.as_view(), name="delete-stories-api"),
    path("stories/view/", StoryViewAPIView.as_view(), name="view-stories-api"),
    path(
        "stories/active/followings/",
        GetUserFollowingStories.as_view(),
        name="get-user-followings-stories-api"
    ),
    path(
        "user/posts/active/",
        GetAuthUserActivePosts.as_view(),
        name="get-auth-user-active-posts-api"
    ),
    path(
        "user/posts/active/<int:id>/",
        GetAuthUserActivePosts.as_view(),
        name="get-auth-user-particular-active-posts-api"
    ),
    path(
        "user/posts/upload/",
        UploadPostAPIView.as_view(),
        name="upload-auth-user-posts-api"
    ),
    path(
        "user/posts/delete/",
        DeletePostAPIView.as_view(),
        name="delete-user-posts-api"
    ),
]
