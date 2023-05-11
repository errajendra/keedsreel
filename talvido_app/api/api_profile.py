from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from talvido_app.models import Profile, Follow, Talvidouser, Point
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
    GetUserPointsModelSerializer,
)


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

class FollowersAPIView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        followers = Follow.objects.select_related().filter(user_to=request.user)
        followers_serializer = FollowersModelSerializer(
            followers, many=True, context={"request": request}
        )
        response = {
            "status_code": status.HTTP_200_OK,
            "message": "ok",
            "data": {
                "users": followers_serializer.data,
                "followers": followers.count(),
            },
        }
        return Response(response, status=status.HTTP_200_OK)


"""This API's will get all the following of a current user"""

class FollowingsAPIView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        following = Follow.objects.select_related().filter(user_from=request.user)
        followings_serializer = FollowingModelSerializer(
            following, many=True, context={"request": request}
        )
        response = {
            "status_code": status.HTTP_200_OK,
            "message": "ok",
            "data": {
                "users": followings_serializer.data,
                "followings": following.count(),
            },
        }
        return Response(response, status=status.HTTP_200_OK)


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
        referral_users  = user.referral_by_user.all()
        referral_user_serializer = GetReferralUserModelSerializer(referral_users, many=True, context={"request": request})
        response = {
            "status_code" : status.HTTP_200_OK,
            "message": "ok",
            "data": referral_user_serializer.data 
        }
        return Response(response, status=status.HTTP_200_OK)


class GetUserPointsAPIView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        points = Point.objects.get(user=request.user)
        user_points_serializer = GetUserPointsModelSerializer(points, context={"request": request})
        response = {
            "status_code" : status.HTTP_200_OK,
            "message": "ok",
            "data": user_points_serializer.data 
        }
        return Response(response, status=status.HTTP_200_OK)
