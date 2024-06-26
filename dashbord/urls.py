from django.urls import path, include
from .views import (
    index, login_view, logout_view, user_list, home,
    post_list, delete_post,
    story_list, delete_story,
    user_profile, delete_user,
    reels_list, reel_delete,
    
)
from .view_ajax import (
    get_users_followers, 
    get_post_comments_or_likes,
    get_reel_comments_or_likes,
    user_account_activation,
)
from .view_payments import (
    view_transaction,
)


urlpatterns = [
    # User Auth URLs
    path("login/", login_view, name='login'),
    path("logout/", logout_view, name='logout'),
    path("view-profile/<str:fid>/", user_profile, name='profile'),
    
    path("", home),
    path("dashbord/", index, name='index'),
    
    path("users/", user_list, name="user_list"),
    path("delete-user/<str:fid>/", delete_user, name="delete_user"),
    
    path("posts/", post_list, name="post_list"),
    path("delete-post/<int:id>/", delete_post, name="delete_post"),
    
    path("stories/", story_list, name="story_list"),
    path("delete-story/<int:id>/", delete_story, name="delete_story"),
    
    path("reels/", reels_list, name="reel_list"),
    path("delete-reel/<int:id>/", reel_delete, name="delete_reel"),
    
    
    # Ajax Urls
    path("ajax-get-user-follow/", get_users_followers, name="get-user-follow-following-users"),
    path("ajax-get-post-likes-comments/", get_post_comments_or_likes, name="get-post-likes-comments"),
    path("ajax-get-reel-likes-comments/", get_reel_comments_or_likes, name="get-reel-likes-comments"),
    # User Account
    path("ajax-activate-deactivate-user/", user_account_activation, name="activate-deactivate-user"),
    
    
    # Payments Urls. 
    path("view-transactions/", view_transaction, name="view-transactions"),
    
]
