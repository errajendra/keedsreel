from django.urls import path, include
from .views import (
    index, login_view, logout_view, user_list
)


urlpatterns = [
    # User Auth URLs
    path("login/", login_view, name='login'),
    path("logout/", logout_view, name='logout'),
    
    path("", index, name='index'),
    path("users/", user_list, name="user_list"),
    
]
