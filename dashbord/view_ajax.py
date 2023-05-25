from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.db.models import Q
from talvido_app.models import Talvidouser as User
from talvido_app.models import (
    Follow, Post, Reel
)


""" Listing of user following follower and friends """
def get_users_followers(request):
    if request.method == "POST":
        try:
            list_type = request.POST.get('list_type')
            user_fid = request.POST.get('user_id')
            user = User.objects.get(firebase_uid=user_fid)
            follows = Follow.objects.select_related().filter(Q(user_to=user) | Q(user_from=user))
            title = "Users"     
            if list_type == "followers":
                users = follows.filter(user_to=user).values('user_from')
                title = "Followers"
            elif list_type == "friends":
                folwers = follows.filter(user_to=user).values('user_from')
                users = follows.filter(user_from=user, user_to__in=folwers).values('user_to')
                title = "Friends"
            elif list_type == "following":
                users = follows.filter(user_from=user).values('user_to')
                title = "Following"
            else:
                print("Not a valid choice")
                users = []
            user_data = User.objects.filter(firebase_uid__in=users)
            html = render_to_string('users/ajax/user-list.html', {'users': user_data})
            response = {
                'title': title,
                'html': html,
                'status': 200
            }
            return JsonResponse(response)
        except Exception as e:
            print(e)
            return JsonResponse({
                "status": 400,
                "error": f"{e}"
            })
    return JsonResponse({
        "status": 405
    })


""" Listing of comments or likes of Post """
def get_post_comments_or_likes(request):
    if request.method == "POST":
        try:
            data_type = request.POST.get('data_choice')
            post_id = request.POST.get('post_id')
            post = get_object_or_404(Post, id=post_id)
            
            if data_type == "likes":
                likes = post.post_like.all().values('user')
                users = User.objects.filter(firebase_uid__in = likes)
                html = render_to_string('users/ajax/user-list.html', {'users': users})
                response = {
                    'title': "Likes",
                    'html': html,
                    'status': 200
                }
            elif data_type == "comments":
                comments = post.post_comment.all()
                html = render_to_string('feed/post/ajax/comments.html', {'comments': comments})
                response = {
                    'title': "Comments",
                    'html': html,
                    'status': 200
                }
            else:
                response = {
                    'title': "Invailid Choiceo of data",
                    'status': 200
                }
            return JsonResponse(response)
        
        except Exception as e:
            print(e)
            return JsonResponse({
                "status": 400,
                "error": f"{e}"
            })
    return JsonResponse({
        "status": 405
    })


""" Listing of comments or likes of Reel """
def get_reel_comments_or_likes(request):
    if request.method == "POST":
        try:
            data_type = request.POST.get('data_choice')
            reel_id = request.POST.get('reel_id')
            reel = get_object_or_404(Reel, id=reel_id)
            
            if data_type == "likes":
                likes = reel.reel_like.all().values('user')
                users = User.objects.filter(firebase_uid__in = likes)
                html = render_to_string('users/ajax/user-list.html', {'users': users})
                response = {
                    'title': "Likes",
                    'html': html,
                    'status': 200
                }
            elif data_type == "comments":
                comments = reel.reelcomment_set.all()
                html = render_to_string('feed/post/ajax/comments.html', {'comments': comments})
                response = {
                    'title': "Comments",
                    'html': html,
                    'status': 200
                }
            else:
                response = {
                    'title': "Invailid Choice of data",
                    'status': 200
                }
            return JsonResponse(response)
        
        except Exception as e:
            print(e)
            return JsonResponse({
                "status": 400,
                "error": f"{e}"
            })
    return JsonResponse({
        "status": 405
    })


""" Activate or deactivate User account """
def user_account_activation(request):
    if request.method == "POST":
        try:
            task = request.POST.get('task')
            user_id = request.POST.get('user_id')
            user = get_object_or_404(User, firebase_uid=user_id)
            if task == "activate":
                user.is_active = True
                user.save()
                message = "User Activated."
            elif task == "deactivate":
                user.is_active = False
                user.save()
                message = "User Deactivated."
            else:
                message = "Internal Server Error."
            response = {
                "status": 200,
                "message": message
            }
        except Exception as e:
            print(e)
            response = {
                "status": 400,
                "error": f"{e}"
            }
        return JsonResponse(response)
    return JsonResponse({
        "status": 405
    })