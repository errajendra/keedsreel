from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.db.models import Q, Max, Sum
from django.contrib.auth.decorators import login_required
from talvido_app.models import Talvidouser as User
from talvido_app.models import (
    Post, Story, Point, Follow
    )



""" Admin Login view with email and password """
def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(Q(email=email) | Q(firebase_uid=email), is_staff = True)
        except User.DoesNotExist:
            messages.warning(request, 'Enter a valid username or email')
            return render(request, 'credential/login.html')
        if user.check_password(password):
            login(request, user)
            next = request.GET.get('next', None)
            if next:
                return redirect(next)
            return redirect('index')
        else:
            messages.warning(request, 'Please enter a valid password.')
            return render(request, 'credential/login.html')
    return render(request, 'credential/login.html')


""" Logout view """
def logout_view(request):
    logout(request)
    return redirect(login_view)
    

""" Dashbord of User view"""
@login_required
def index(request):
    """
        Dashboard- show total number of posts, stories, users.
        User with highest point, recent point activity 
    """
    post_count = Post.objects.count()
    story_count = Story.objects.count()
    user_count = User.objects.count()
    points = Point.objects.select_related()
    
    # User with highest point
    highest_point_users = points.order_by('-points')[:10]
    recent_points = points.order_by('-created_at')[:10]
    
    context = {
        "title": "Dashbord",
        "post_count": post_count,
        "user_count": user_count,
        "story_count": story_count,
        "recent_points": recent_points,
        "highest_point_users": highest_point_users,
    }
    return render(request, 'dashbord.html', context)


""" Base url redirect to dashbord. """
def home(request):
    return redirect(index)


""" 
User Views 
"""
"""List of all Users """
@login_required
def user_list(request):
    users = User.objects.select_related().order_by('-date_joined')
    context = {
        "title": "All Users",
        'users': users
    }
    return render(request, 'users/list.html', context)


""" User Profile """
def user_profile(request, fid):
    user = User.objects.select_related().get(firebase_uid=fid)
    follows = Follow.objects.filter(Q(user_to=user) | Q(user_from=user))
    follower = follows.filter(user_to=user).values('user_from')
    following = follows.filter(user_from=user)
    friends = following.filter(user_to__in=follower)
    posts = user.post_user.all()
    stories = user.story_set.all()
    context = {
        "title": "User Profile",
        "user": user,
        "follower": follower.count(),
        "following": following.count(),
        "friends": friends.count(),
        "posts": posts,
        "stories": stories,
    }
    return render(request, 'users/profile.html', context)



""" 
Post View 
"""
""" List of all Posts """
@login_required
def post_list(request):
    posts = Post.objects.select_related().order_by('-updated_at')
    context = {
        "title": "All Posts",
        'posts': posts
    }
    return render(request, 'feed/post/list.html', context)



"""
Story View
"""
""" List of all Story """
@login_required
def story_list(request):
    stories = Story.objects.select_related().order_by('-updated_at')
    context = {
        "title": "All Stories",
        'stories': stories
    }
    return render(request, 'feed/story/list.html', context)

