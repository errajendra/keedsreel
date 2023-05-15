from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.db.models import Q, Max, Sum
from django.contrib.auth.decorators import login_required
from talvido_app.models import Talvidouser as User
from talvido_app.models import Post, Story, Point



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
@login_required(login_url='login')
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
    return render(request, 'index.html', context)


def home(request):
    return redirect(index)


""" List of all Users """
@login_required
def user_list(request):
    users = User.objects.select_related().order_by('-date_joined')
    context = {
        "title": "All Users",
        'users': users
    }
    print(dir(users.first()))
    return render(request, 'users/list.html', context)

