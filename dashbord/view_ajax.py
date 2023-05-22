from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Q
from talvido_app.models import Talvidouser as User
from talvido_app.models import Follow


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

