from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from talvido_app.models import Profile, Follow, Talvidouser
from rest_framework.permissions import IsAuthenticated
from talvido_app.firebase.authentication import FirebaseAuthentication
from . import (
    ProfileModelSerializer,
    UpdateProfileModelSerializer,
    UpdateuserProfilePictureModelSerializer,
    FollowersModelSerializer,
    FollowingModelSerializer,
    UserFollowSerializer,
    GetReferralUserModelSerializer,
    GetPostCommentModelSerializer,
    GetPostLikeModelSerializer,
    TimeSpendsModelSerializer,
)
from talvido_app.pagination import PageNumberPaginationView


"""This api will update and get the 
    profile information of the user"""

class ProfileAPIView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def get_profile(self, request):
        """get the profile of user"""
        profile = Profile.objects.get(user=request.user)
        return profile

    def get(self, request):
        """serializer the data"""
        profile_serializer = ProfileModelSerializer(
            self.get_profile(request), context={"request": request}
        )

        response = {
            "status_code": status.HTTP_200_OK,
            "message": "ok",
            "data": profile_serializer.data,
        }
        return Response(response, status=status.HTTP_200_OK)

    def patch(self, request):
        update_profile_serializer = UpdateProfileModelSerializer(
            instance=self.get_profile(request), data=request.data, partial=True
        )

        if update_profile_serializer.is_valid():
            update_profile_serializer.save()
            response = {"status_code": status.HTTP_200_OK, "message": "profile updated"}
            return Response(response, status=status.HTTP_200_OK)

        response = {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": "bad request",
            "data": update_profile_serializer.errors,
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


"""This API will update the profile picture of an user"""

class UpdateProfilePictureAPIView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def get_profile(self, request):
        """get the profile of user"""
        profile = Profile.objects.get(user=request.user)
        return profile

    def put(self, request):
        upadate_profile_pic_serializer = UpdateuserProfilePictureModelSerializer(
            instance=self.get_profile(request), data=request.data
        )

        if upadate_profile_pic_serializer.is_valid():
            profile = upadate_profile_pic_serializer.save()
            response = {
                "status_code": status.HTTP_200_OK,
                "message": "profile picture updated",
                "data": {
                    "image": ProfileModelSerializer(
                        profile, context={"request": request}
                    ).data["image"]
                },
            }
            return Response(response, status=status.HTTP_200_OK)

        response = {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": "bad request",
            "data": upadate_profile_pic_serializer.errors,
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


"""This API will remove the user profile picture"""

class RemoveProfilePictureAPIView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def get_profile(self, request):
        """get the profile of user"""
        profile = Profile.objects.get(user=request.user)
        return profile

    def put(self, request):
        profile_image = self.get_profile(request)
        profile_image.image = "default.png"
        profile_image.save()
        response = {
            "status_code": status.HTTP_200_OK,
            "message": "profile picture updated",
            "data": {
                "image": ProfileModelSerializer(
                    profile_image, context={"request": request}
                ).data["image"]
            },
        }
        return Response(response, status=status.HTTP_200_OK)


"""This API's will get all the followers of a current user"""

class FollowersAPIView(APIView, PageNumberPaginationView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    page_size = 10

    def get(self, request, firebase_uid=None):
        if firebase_uid is None:
            followers = (
                Follow.objects.select_related()
                .filter(user_to=request.user)
                .order_by("created_at")
            )
        else:
            try:
                user = Talvidouser.objects.get(firebase_uid=firebase_uid)
            except Talvidouser.DoesNotExist:
                response = {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": "bad request",
                    "data": {"firebase_uid": ["firebase_uid is invalid"]},
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            followers = (
                Follow.objects.select_related()
                .filter(user_to=user)
                .order_by("created_at")
            )
        results = self.paginate_queryset(followers, request, view=self)
        followers_serializer = FollowersModelSerializer(
            results, many=True, context={"request": request}
        )
        return self.get_paginated_response(followers_serializer.data)


"""This API's will get all the following of a current user"""

class FollowingsAPIView(APIView, PageNumberPaginationView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    page_size = 10

    def get(self, request, firebase_uid=None):
        if firebase_uid is None:
            followings = (
                Follow.objects.select_related()
                .filter(user_from=request.user)
                .order_by("created_at")
            )
        else:
            try:
                user = Talvidouser.objects.get(firebase_uid=firebase_uid)
            except Talvidouser.DoesNotExist:
                response = {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": "bad request",
                    "data": {"firebase_uid": ["firebase_uid is invalid"]},
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            followings = (
                Follow.objects.select_related()
                .filter(user_from=user)
                .order_by("created_at")
            )

        results = self.paginate_queryset(followings, request, view=self)
        followings_serializer = FollowingModelSerializer(
            results, many=True, context={"request": request}
        )
        return self.get_paginated_response(followings_serializer.data)


"""This API's will get the any user profile using its firebase uid"""

class GetAnyUserProfileAPIView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, firebase_uid):
        try:
            profile = Profile.objects.get(user=firebase_uid)
        except Profile.DoesNotExist:
            response = {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": "bad request",
                "data": {"firebase_uid": ["firebase_uid is invalid or doesn't exists"]},
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        user_serializer = ProfileModelSerializer(profile, context={"request": request})
        response = {
            "status_code": status.HTTP_200_OK,
            "message": "ok",
            "data": user_serializer.data,
        }
        return Response(response, status=status.HTTP_200_OK)


"""This API will follow and unfollow user"""

class UserFollowAPIView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_follow_serializer = UserFollowSerializer(
            data=request.data, context={"request": request}
        )
        if user_follow_serializer.is_valid():
            user_follow_serializer.save()
            response = {
                "status_code": status.HTTP_201_CREATED,
                "message": "user follow",
            }
            return Response(response, status=status.HTTP_201_CREATED)

        response = {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": "bad request",
            "data": user_follow_serializer.errors,
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user_unfollow_serializer = UserFollowSerializer(
            data=request.data, context={"request": request}
        )
        if user_unfollow_serializer.is_valid():
            user_unfollow_serializer.delete()
            response = {
                "status_code": status.HTTP_204_NO_CONTENT,
                "message": "user unfollow",
            }
            return Response(response, status=status.HTTP_204_NO_CONTENT)

        response = {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": "bad request",
            "data": user_unfollow_serializer.errors,
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

class GetUserReferralAPIView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = Talvidouser.objects.get(firebase_uid=request.user)
        referral_users = user.referral_by_user.all()
        referral_user_serializer = GetReferralUserModelSerializer(
            referral_users, many=True, context={"request": request}
        )
        response = {
            "status_code": status.HTTP_200_OK,
            "message": "ok",
            "data": {
                "referral_users": referral_user_serializer.data,
                "image": "https://"
                + request.META["HTTP_HOST"]
                + request.user.profile.image.url,
                "total_score": referral_users.count(),
                "total_referred_users": referral_users.count(),
            },
        }
        return Response(response, status=status.HTTP_200_OK)


"""This API will remove user follower"""

class RemoveUserFollowerAPIView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, firebase_uid):
        try:
            follower_user = Talvidouser.objects.get(firebase_uid=firebase_uid)
        except Talvidouser.DoesNotExist:
            response = {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": "bad request",
                "data": {"firebase_uid": ["firebase_uid is invalid"]},
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        follower = Follow.objects.filter(user_to=request.user, user_from=follower_user)
        if follower.exists():
            follower.first().delete()
            response = {
                "status_code": status.HTTP_204_NO_CONTENT,
                "message": "removed follower",
            }
            return Response(response, status=status.HTTP_204_NO_CONTENT)

        response = {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": "it's not your follower",
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


"""This API will get recent user post likes"""

class UserPostLikeActivityAPIView(APIView, PageNumberPaginationView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    page_size = 12

    def get(self, request):
        user = Talvidouser.objects.get(firebase_uid=request.user)
        user_post_likes = user.post_like_user.all().order_by("-created_at")
        liked_posts_paginate = self.paginate_queryset(
            user_post_likes, request, view=self
        )
        liked_posts_serializer = GetPostLikeModelSerializer(
            liked_posts_paginate, many=True, context={"request": request}
        )
        return self.get_paginated_response(liked_posts_serializer.data)


"""This API will get recent user post comments"""

class UserPostCommentActivityAPIView(APIView, PageNumberPaginationView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    page_size = 10

    def get(self, request):
        user = Talvidouser.objects.get(firebase_uid=request.user)
        user_post_comments = user.post_comment_user.all().order_by("-created_at")
        comment_posts_paginate = self.paginate_queryset(
            user_post_comments, request, view=self
        )
        comment_posts_serializer = GetPostCommentModelSerializer(
            comment_posts_paginate, many=True, context={"request": request}
        )
        return self.get_paginated_response(comment_posts_serializer.data)


class UserTimeSpendsWeekAPIView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = Talvidouser.objects.get(firebase_uid=request.user)
        time_spends_week = user.user_time_spends.all().order_by("-created_at")[:7]
        time_spends_week_serializer = TimeSpendsModelSerializer(time_spends_week, many=True)
        response = {
            "status_code": status.HTTP_200_OK,
            "message": "ok",
            "data": time_spends_week_serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)
