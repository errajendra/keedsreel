from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.db.models import Q, Max, Sum
from django.contrib.auth.decorators import login_required
from talvido_app.models import Talvidouser as User
from talvido_app.models import (
    Post, Story, Point, Follow, Reel
    )
from mlm.api.helpers import UserLevel
from mlm.models import Level


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
            next_url = request.GET.get('next', None)
            if next_url:
                return redirect(next_url)
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


@login_required
def delete_user(request, fid):
    user = get_object_or_404(User, firebase_uid=fid)
    if user:
        user.delete()
    return redirect(user_list)
    

""" User Profile """
@login_required
def user_profile(request, fid):
    try:
        user = User.objects.select_related().get(firebase_uid=fid)
    except User.DoesNotExist:
        return HttpResponseNotFound()
    follows = Follow.objects.filter(Q(user_to=user) | Q(user_from=user))
    follower = follows.filter(user_to=user).values('user_from').count()
    following = follows.filter(user_from=user).count()
    friends = follows.filter(user_from=user, user_to__in=follows.filter(user_to=user).values('user_from')).count()
    posts = user.post_user.all()
    stories = user.story_set.all()
    reels = user.reel_user.all()
    # MLM
    level = UserLevel(user=user)
    try:
        next_level = Level.objects.get(level=level.get_user_level+1)
    except:
        next_level = Level.objects.get(level=level.get_user_level)
    level_data = {
        "at_level": level.get_user_level,
        "at_level_referral": level.get_current_level_referral_users,
        "total_referral_user": level.get_total_referral_users,
        "next_level": next_level.level,
        "next_level_referral": next_level.referral_users,
        "process_to_next_percent": level.get_total_referral_users*100/next_level.referral_users,
    }
    
    context = {
        "title": "User Profile",
        "user": user,
        "follower": follower,
        "following": following,
        "friends": friends,
        "posts": posts,
        "stories": stories,
        "reels": reels,
        "level": level_data,
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


""" Delete a post by id."""
@login_required
def delete_post(request, id):
    post = get_object_or_404(Post, id=id)
    if post:
        post.delete()
    return redirect(post_list)
    


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


""" Delete a story by id."""
@login_required
def delete_story(request, id):
    ins = get_object_or_404(Story, id=id)
    if ins:
        ins.delete()
    return redirect(story_list)
    


"""
Reel View
"""
""" List of all reels """
@login_required
def reels_list(request):
    reels = Reel.objects.select_related().order_by('-updated_at')
    print(dir(reels[0]))
    context = {
        "title": "Reels",
        'reels': reels
    }
    return render(request, 'feed/reel/list.html', context)


@login_required
def reel_delete(request, id):
    reel = get_object_or_404(Reel, id=id)
    if reel:
        reel.delete()
    return redirect(reels_list)

