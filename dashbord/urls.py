from django.urls import path, include
from .views import (
    index, login_view, logout_view, user_list, home,
    post_list, delete_post,
    story_list, delete_story,
    user_profile, delete_user,
    reels_list, reel_delete,
    
)
from .view_ajax import get_users_followers


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
    path("ajax-get-user-follow/", get_users_followers, name="ajax_login"),
]
