from django.urls import path, include
from .views import (
    index, login_view, logout_view, user_list, home, post_list, story_list,
    user_profile
)


urlpatterns = [
    # User Auth URLs
    path("login/", login_view, name='login'),
    path("logout/", logout_view, name='logout'),
    path("view-profile/<str:fid>/", user_profile, name='profile'),
    
    path("", home),
    path("dashbord/", index, name='index'),
    path("users/", user_list, name="user_list"),
    path("posts/", post_list, name="post_list"),
    path("stories/", story_list, name="story_list"),
    
]
