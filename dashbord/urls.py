from django.urls import path, include
from .views import (
    index, login_view, logout_view, user_list, home, post_list, story_list,
    user_profile, delete_user
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
    path("stories/", story_list, name="story_list"),
    
]
