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
    ResetEmailPasswordAPIView,
    ChangeEmailPasswordAPIView,
    ProfileAPIView,
    UserTimeSpendsWeekAPIView,
    UserTimeSpendsTodayAPIView,
    GetUserReferralAPIView,
    UpdateProfilePictureAPIView,
    RemoveProfilePictureAPIView,
    UserFollowAPIView,
    FollowersAPIView,
    FollowingsAPIView,
    RemoveUserFollowerAPIView,
    GetAnyUserProfileAPIView,
    UserPostLikeActivityAPIView,
    UserPostCommentActivityAPIView,
    ActiveStoryAPIView,
    ArchiveStoryAPIView,
    CreateStoryAPIView,
    DeleteStoryAPIView,
    StoryViewAPIView,
    GetUserFollowingStories,
    GetAuthUserActivePosts,
    UploadPostAPIView,
    DeletePostAPIView,
    GetUserAllPosts,
    PostCommentAPIView,
    DeletePostCommentAPIView,
    AddPostLikeAPIView,
    RemovePostLikeAPIView,
    GetUserFollowingsPost,
    AddPostCommentLikeAPIView,
    RemovePostCommentLikeAPIView,
    SearchAccountAPIView,
    GetStoryHighlightsAPIView,
    GetUserReelsAPIView,
    UploadUserReelsAPIView,
    GetUsersAllReelsAPIView,
    GetTrendingReelsAPIView,
    SearchPostAPIView,
    AddReelViewAPIView,
    AddReelLikeAPIView,
    RemoveReelLikeAPIView,
    AddReelCommentAPIView,
    RemoveReelCommentAPIView,
    AddReelCommentLikeAPIView,
    RemoveReelCommentLikeAPIView,
    DeleteUserReelAPIView,
    BankDetailsAPIView,
    BankPaymentAPIView,
    CompanyPaymentInfoAPIView,
    UPIPaymentAPIView,
    UserSubscriptionAPIView,
    RecentAccountSearchAPIView,
    NotificationAPIView,
    SeenNotificationAPIView,
    # GoogleTokenAuthAPIView,
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
    path("auth/google-auth/", LoginGoogleAPIView.as_view(), name="login-google-api"),
    path("auth/login/google/", LoginGoogleAPIView.as_view(), name="login-google-base-api"),
    # path(
    #     "auth/google-auth/",
    #     GoogleTokenAuthAPIView.as_view(),
    #     name="auth-google-api"
    # ),
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
    path(
        "auth/email/reset/password/",
        ResetEmailPasswordAPIView.as_view(),
        name="reset-email-password-api",
    ),
    path(
        "auth/email/change/password/",
        ChangeEmailPasswordAPIView.as_view(),
        name="change-email-password-api",
    ),
    # profile api's endpoints
    path(
        "user/profile/", ProfileAPIView.as_view(), name="get-current-user-profile-api"
    ),
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
    path(
        "user/profile/followers/", FollowersAPIView.as_view(), name="user-followers-api"
    ),
    path(
        "user/profile/followings/",
        FollowingsAPIView.as_view(),
        name="user-followings-api",
    ),
    path(
        "user/profile/followers/<str:firebase_uid>/",
        FollowersAPIView.as_view(),
        name="user-followers-api",
    ),
    path(
        "user/remove/follower/<str:firebase_uid>/",
        RemoveUserFollowerAPIView.as_view(),
        name="user-remove-follower-api",
    ),
    path(
        "user/profile/followings/<str:firebase_uid>/",
        FollowingsAPIView.as_view(),
        name="user-followings-api",
    ),
    path(
        "user/profile/<str:firebase_uid>/",
        GetAnyUserProfileAPIView.as_view(),
        name="get-any-user-profile-api",
    ),
    path("user/follow/", UserFollowAPIView.as_view(), name="user-follow-api"),
    path(
        "user/referrals/", GetUserReferralAPIView.as_view(), name="user-referrals-api"
    ),
    path(
        "user/post/activity/likes/", UserPostLikeActivityAPIView.as_view(), name="user-post-like-activity-api"
    ),
    path(
        "user/post/activity/comments/", UserPostCommentActivityAPIView.as_view(), name="user-post-comment-activity-api"
    ),
    path(
        "user/time-spends/week/", UserTimeSpendsWeekAPIView.as_view(), name="user-time-spends-week-api"
    ),
     path(
        "user/time-spends/today/", UserTimeSpendsTodayAPIView.as_view(), name="user-time-spends-today-api"
    ),
    # post API's enpoints
    path("stories/active/", ActiveStoryAPIView.as_view(), name="active-stories-api"),
    path("stories/archive/", ArchiveStoryAPIView.as_view(), name="archive-stories-api"),
    path("stories/create/", CreateStoryAPIView.as_view(), name="create-stories-api"),
    path("stories/delete/", DeleteStoryAPIView.as_view(), name="delete-stories-api"),
    path("stories/view/", StoryViewAPIView.as_view(), name="view-stories-api"),
    path(
        "stories/active/followings/",
        GetUserFollowingStories.as_view(),
        name="get-user-followings-stories-api",
    ),
    path(
        "user/posts/active/",
        GetAuthUserActivePosts.as_view(),
        name="get-auth-user-active-posts-api",
    ),
    path(
        "user/posts/active/<int:id>/",
        GetAuthUserActivePosts.as_view(),
        name="get-auth-user-particular-active-posts-api",
    ),
    path(
        "user/posts/all/",
        GetUserAllPosts.as_view(),
        name="get-user-all-posts-api",
    ),
    path(
        "user/posts/upload/",
        UploadPostAPIView.as_view(),
        name="upload-auth-user-posts-api",
    ),
    path(
        "user/posts/delete/", DeletePostAPIView.as_view(), name="delete-user-posts-api"
    ),
    path(
        "stories/highlights/",
        GetStoryHighlightsAPIView.as_view(),
        name="stories-highlights-api",
    ),
    # comment API'S endpoints
    path(
        "post/comment/add/", PostCommentAPIView.as_view(), name="add-post-comment-api"
    ),
    path(
        "post/comment/delete/",
        DeletePostCommentAPIView.as_view(),
        name="delete-post-comment-api",
    ),
    path("post/like/add/", AddPostLikeAPIView.as_view(), name="add-post-like-api"),
    path(
        "post/like/remove/",
        RemovePostLikeAPIView.as_view(),
        name="remove-post-like-api",
    ),
    path(
        "user/posts/followings/",
        GetUserFollowingsPost.as_view(),
        name="get-user-following-post-api",
    ),
    path(
        "post/comment/add/like/",
        AddPostCommentLikeAPIView.as_view(),
        name="add-post-comment-like-api",
    ),
    path(
        "post/comment/remove/like/",
        RemovePostCommentLikeAPIView.as_view(),
        name="remove-post-comment-like-api",
    ),
    # search API
    path("search/account/", SearchAccountAPIView.as_view(), name="search-account-api"),
    path("search/post/", SearchPostAPIView.as_view(), name="search-post-api"),
    path(
        "search/recent/add/",
        RecentAccountSearchAPIView.as_view(),
        name="add-recent-account-search-api",
    ),
    path(
        "search/recent/",
        RecentAccountSearchAPIView.as_view(),
        name="recent-account-search-api",
    ),
    path(
        "search/recent/delete/",
        RecentAccountSearchAPIView.as_view(),
        name="delete-recent-account-search-api",
    ),
    # reels API
    path(
        "user/reels/active/",
        GetUserReelsAPIView.as_view(),
        name="get-current-user-all-reels-api",
    ),
    path(
        "user/reels/active/<int:id>/",
        GetUserReelsAPIView.as_view(),
        name="get-particular-reels-api",
    ),
    path(
        "users/reels/",
        GetUsersAllReelsAPIView.as_view(),
        name="get-users-all-reels-api",
    ),
    path(
        "trending/reels/",
        GetTrendingReelsAPIView.as_view(),
        name="get-trending-reels-api",
    ),
    path(
        "user/reels/upload/",
        UploadUserReelsAPIView.as_view(),
        name="upload-current-user-reels-api",
    ),
    path("reels/views/add/", AddReelViewAPIView.as_view(), name="add-reel-view-api"),
    path("reels/like/add/", AddReelLikeAPIView.as_view(), name="add-reel-like-api"),
    path(
        "reels/like/remove/<int:id>/",
        RemoveReelLikeAPIView.as_view(),
        name="remove-reel-like-api",
    ),
    path(
        "reels/comment/add/",
        AddReelCommentAPIView.as_view(),
        name="add-reel-comment-api",
    ),
    path(
        "reels/comment/remove/",
        RemoveReelCommentAPIView.as_view(),
        name="remove-reel-comment-api",
    ),
    path(
        "reels/comment/add/like/",
        AddReelCommentLikeAPIView.as_view(),
        name="add-reel-comment-like-api",
    ),
    path(
        "reels/comment/remove/like/",
        RemoveReelCommentLikeAPIView.as_view(),
        name="remove-reel-comment-like-api",
    ),
    path(
        "user/reels/delete/<int:id>/",
        DeleteUserReelAPIView.as_view(),
        name="delete-user-reel-api",
    ),
    # payment api
    path("user/bank/", BankDetailsAPIView.as_view(), name="user-bank-details-api"),
    path(
        "user/bank/upload/payment/",
        BankPaymentAPIView.as_view(),
        name="user-bank-payment-api",
    ),
    path(
        "user/upi/upload/payment/",
        UPIPaymentAPIView.as_view(),
        name="user-upi-payment-api",
    ),
    path(
        "company/payment/info/",
        CompanyPaymentInfoAPIView.as_view(),
        name="company-payment-info-api",
    ),
    path(
        "user/subscription/",
        UserSubscriptionAPIView.as_view(),
        name="user-subscription-api",
    ),
    path(
        "user/notification/",
        NotificationAPIView.as_view(),
        name="user-notiication-api",
    ),
    path(
        "user/notification/seen/",
        SeenNotificationAPIView.as_view(),
        name="user-notiication-seen-api",
    ),
]
