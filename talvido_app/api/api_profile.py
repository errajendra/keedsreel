from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from talvido_app.models import Profile, Follow
from rest_framework.permissions import IsAuthenticated
from talvido_app.firebase.authentication import FirebaseAuthentication
from . import (
    ProfileModelSerializer,
    UpdateProfileModelSerializer,
    UpdateuserProfilePictureModelSerializer,
    FollowersModelSerializer,
    FollowingModelSerializer
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
    
    def put(self,request):
        profile_image = self.get_profile(request)
        profile_image.image = "default.png"
        profile_image.save()
        response = {
                "status_code": status.HTTP_200_OK,
                "message": "profile picture updated",
                "data": {
                    "image": ProfileModelSerializer(
                        profile_image, context={"request": request}
                    ).data['image']
                },
            }
        return Response(response, status=status.HTTP_200_OK)



"""This API's will get all the followers of a current user"""

class FollowersAPIView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        followers = Follow.objects.select_related().filter(user_to=request.user)
        followers_serializer = FollowersModelSerializer(followers,many=True)
        response = {
            "status_code" : status.HTTP_200_OK,
            "message" : "ok",
            "data" : {
                "users" : followers_serializer.data,
                'followers': followers.count()   
            }
        }
        return Response(response,status=status.HTTP_200_OK)


"""This API's will get all the following of a current user"""

class FollowingsAPIView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        following = Follow.objects.select_related().filter(user_from=request.user)
        followings_serializer = FollowingModelSerializer(following,many=True)
        response = {
            "status_code" : status.HTTP_200_OK,
            "message" : "ok",
            "data" : {
                "users" : followings_serializer.data,
                'followings': following.count()   
            }
        }
        return Response(response,status=status.HTTP_200_OK)
