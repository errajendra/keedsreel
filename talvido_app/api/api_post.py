from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from talvido_app.models import Story, StoryViews, Follow, Talvidouser, Post
from rest_framework.permissions import IsAuthenticated
from talvido_app.firebase.authentication import FirebaseAuthentication
from . import (
    StoryModelSerializer,
    DeleteStorySerializer,
    StoryViewModelSerializer,
    AddStoryViewSerializer,
    GetUserFollowingsStoriesModelSerializer,
    GetPostModelSerializer,
    UploadPostModelSerializer,
    DeletePostSerializer,
    PostCommentModelSerializer,
    DeletePostCommentSerializer,
    AddPostLikeSerializer,
    AddPostCommentLikeSerializer,
    GetStoryHighlightsModelSerializer,
    GetPostCommentModelSerializer,
)
from rest_framework.parsers import (
    MultiPartParser,
    JSONParser,
    FormParser,
    FileUploadParser,
)
from datetime import datetime
from talvido_app.pagination import PageNumberPaginationView
import logging
from talvido_app.imagekit.main import ImagekitClient


# Get an instance of a logger
logger = logging.getLogger(__name__)


"""This api return the active stories of an user"""

class ActiveStoryAPIView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """filter the active stories of current user"""
        story = Story.objects.select_related().filter(
            user=request.user, ends_at__gt=datetime.today()
        )
        """serialize the data"""
        story_serializer = StoryModelSerializer(
            story, many=True, context={"request": request}
        )
        response = {
            "status_code": status.HTTP_200_OK,
            "message": "ok",
            "data": story_serializer.data,
        }
        return Response(response, status=status.HTTP_200_OK)


"""This api return the archive stories of an user"""

class ArchiveStoryAPIView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """filter archive stories of current user"""
        story = Story.objects.filter(user=request.user)
        """serialize the data"""
        story_serializer = StoryModelSerializer(
            story, many=True, context={"request": request}
        )
        response = {
            "status_code": status.HTTP_200_OK,
            "message": "ok",
            "data": story_serializer.data,
        }
        return Response(response, status=status.HTTP_200_OK)


"""This api will create a new story"""

class CreateStoryAPIView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """deserialize the data"""
        create_story_serializer = StoryModelSerializer(data=request.data, context={"request": request})
        """checking the validation on data"""
        if create_story_serializer.is_valid():
            create_story_serializer.save(user=request.user)
            response = {"status_code": status.HTTP_201_CREATED, "message": "ok"}
            return Response(response, status=status.HTTP_201_CREATED)

        """return this if validation fails"""
        response = {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": "bad request",
            "data": create_story_serializer.errors,
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


"""This api will delete the story"""

class DeleteStoryAPIView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        """deserialize the data"""
        delete_story_serializer = DeleteStorySerializer(data=request.data)
        """checking the validation on data"""
        if delete_story_serializer.is_valid():
            """get the story id"""
            story_id = delete_story_serializer.validated_data.get("story_id")
            """checking the story is belong to the current user or not"""
            if Story.objects.filter(user=request.user, id=story_id).exists():
                delete_story_serializer.delete()
                response = {
                    "status_code": status.HTTP_204_NO_CONTENT,
                    "message": "story deleted",
                }
                return Response(response, status=status.HTTP_204_NO_CONTENT)
            else:
                """response this if story is not belong to the current user or story id is invalid"""
                response = {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": "bad request",
                    "data": {
                        "story_id": [
                            "The story id is either invalid nor associate with current user"
                        ]
                    },
                }
                return Response(response, status=status.HTTP_204_NO_CONTENT)

        """return this response if validation fails"""
        response = {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": "badd request",
            "data": delete_story_serializer.errors,
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


"""This API will get the views and add the views to the story"""

class StoryViewAPIView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            story_id = request.query_params.get("story_id")
            story_view = StoryViews.objects.select_related().filter(story=story_id)
            story_view_serializer = StoryViewModelSerializer(
                story_view, many=True, context={"request": request}
            )
            response = {
                "status_code": status.HTTP_200_OK,
                "message": "ok",
                "data": {
                    "users": story_view_serializer.data,
                    "story_views": story_view.count(),
                },
            }
            return Response(response, status=status.HTTP_200_OK)
        except:
            response = {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": "bad request",
                "data": {
                    "story_id": [
                        "The story_id query params is invalid, make sure it should be integer like (1, 2, 3)"
                    ]
                },
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        add_storyview_serializer = AddStoryViewSerializer(
            data=request.data, context={"request": request}
        )
        if add_storyview_serializer.is_valid():
            add_storyview_serializer.save()
            response = {"status": status.HTTP_201_CREATED, "message": "ok"}
            return Response(response, status=status.HTTP_201_CREATED)

        """return this response if validation fails"""
        response = {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": "badd request",
            "data": add_storyview_serializer.errors,
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


"""This api will get the user following stories"""

class GetUserFollowingStories(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        following_stories = Follow.objects.select_related().filter(user_from=request.user)
        active_stories = Story.objects.select_related().filter(
            user__in=following_stories.values_list("user_to", flat=True), ends_at__gt=datetime.today()
        ).distinct("user")
        followings_stories_serializer = GetUserFollowingsStoriesModelSerializer(
            active_stories, many=True, context={"request": request}
        )
        response = {
            "status_code" : status.HTTP_200_OK,
            "message" : "ok",
            "data" : followings_stories_serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)


"""This APi will show all the active posts of authenticated user"""

class GetAuthUserActivePosts(APIView, PageNumberPaginationView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    page_size = 9    
    def get(self, request, id=None):
        user = Talvidouser.objects.get(firebase_uid=request.user)
        if id is not None:
            try:
                post = user.post_user.get(id=id)
            except Post.DoesNotExist:
                response = {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": "bad request",
                    "data": {
                        "post_id": [
                            "The post id is either invalid nor associate with current user"
                        ]
                    },
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            post_serializer = GetPostModelSerializer(post, context={"request": request})
            response = {
                "status_code": status.HTTP_200_OK,
                "message": "ok",
                "data": post_serializer.data,
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            posts = user.post_user.all().order_by("-created_at")
            posts_paginated = self.paginate_queryset(posts, request, view=self)
            post_serializer = GetPostModelSerializer(
                posts_paginated, many=True, context={"request": request}
            )
            return self.get_paginated_response(post_serializer.data)


"""This API will upload post for authenticated user"""

class UploadPostAPIView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, JSONParser, FileUploadParser, FormParser]

    def post(self, request):
        upload_post_serializer = UploadPostModelSerializer(data=request.data, context={"request": request})
        if upload_post_serializer.is_valid():
            post = upload_post_serializer.save(user=request.user)
            response = {
                "status_code": status.HTTP_201_CREATED,
                "message": "ok",
                "data": {
                    "image": post.post.name
                },
            }
            return Response(response, status=status.HTTP_201_CREATED)

        response = {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": "bad request",
            "data": upload_post_serializer.errors,
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


"""This api will delete the post"""

class DeletePostAPIView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        """deserialize the data"""
        delete_post_serializer = DeletePostSerializer(data=request.data)
        """checking the validation on data"""
        if delete_post_serializer.is_valid():
            """get the post id"""
            post_id = delete_post_serializer.validated_data.get("post_id")
            """checking the post is belong to the current user or not"""
            if Post.objects.filter(user=request.user, id=post_id).exists():
                delete_post_serializer.delete()
                response = {
                    "status_code": status.HTTP_204_NO_CONTENT,
                    "message": "post deleted",
                }
                return Response(response, status=status.HTTP_204_NO_CONTENT)
            else:
                """response this if post is not belong to the current user or post id is invalid"""
                response = {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": "bad request",
                    "data": {
                        "post_id": [
                            "The post id is either invalid nor associate with current user"
                        ]
                    },
                }
                return Response(response, status=status.HTTP_204_NO_CONTENT)

        """return this response if validation fails"""
        response = {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": "bad request",
            "data": delete_post_serializer.errors,
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


"""This API will add the comment to post"""

class PostCommentAPIView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        post_comment_serializer = PostCommentModelSerializer(
            data=request.data, context={"request": request}
        )
        if post_comment_serializer.is_valid():
            post_comment = post_comment_serializer.save()
            response = {
                "status_code": status.HTTP_201_CREATED,
                "message": "comment created",
                "data" : GetPostCommentModelSerializer(post_comment, context={"request": request}).data
            }
            return Response(response, status=status.HTTP_201_CREATED)

        response = {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": "bad request",
            "data": post_comment_serializer.errors,
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


"""This API will delete the comment from post"""

class DeletePostCommentAPIView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        delete_post_comment_serializer = DeletePostCommentSerializer(
            data=request.data, context={"request": request}
        )
        if delete_post_comment_serializer.is_valid():
            delete_post_comment_serializer.delete()
            response = {
                "status_code": status.HTTP_204_NO_CONTENT,
                "message": "comment deleted",
            }
            return Response(response, status=status.HTTP_204_NO_CONTENT)

        response = {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": "bad request",
            "data": delete_post_comment_serializer.errors,
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


"""This API will add like to post"""

class AddPostLikeAPIView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        add_post_like_serializer = AddPostLikeSerializer(
            data=request.data, context={"request": request}
        )
        if add_post_like_serializer.is_valid():
            add_post_like_serializer.save()
            response = {
                "status_code": status.HTTP_201_CREATED,
                "messages": "liked post",
            }
            return Response(response, status=status.HTTP_201_CREATED)

        response = {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": "bad request",
            "data": add_post_like_serializer.errors,
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


"""This API will remove like from post"""

class RemovePostLikeAPIView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        add_post_like_serializer = AddPostLikeSerializer(
            data=request.data, context={"request": request}
        )
        if add_post_like_serializer.is_valid():
            add_post_like_serializer.delete()
            response = {
                "status_code": status.HTTP_204_NO_CONTENT,
                "messages": "liked removed",
            }
            return Response(response, status=status.HTTP_204_NO_CONTENT)

        response = {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": "bad request",
            "data": add_post_like_serializer.errors,
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


"""This API will get all the posts of user followings"""

class GetUserFollowingsPost(APIView, PageNumberPaginationView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    page_size = 2
    def get(self, request):
        user = Talvidouser.objects.get(firebase_uid=request.user)
        followings = user.user_from.all()
        posts = Post.objects.select_related().filter(
            user__in=followings.values_list("user_to", flat=True)
        ).order_by("-created_at")
        if posts.count() < 1:
            posts = Post.objects.select_related().order_by("-created_at")
        results = self.paginate_queryset(posts, request, view=self)
        followings_serializer = GetPostModelSerializer(results, many=True, context={"request": request})
        return self.get_paginated_response(followings_serializer.data)
       

"""This API will add like to post comment"""

class AddPostCommentLikeAPIView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        add_post_comment_like_serializer = AddPostCommentLikeSerializer(
            data=request.data, context={"request": request}
        )

        if add_post_comment_like_serializer.is_valid():
            add_post_comment_like_serializer.save()
            response = {
                "status_code": status.HTTP_201_CREATED,
                "message": "comment like added",
            }
            return Response(response, status=status.HTTP_201_CREATED)

        response = {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": "bad request",
            "data": add_post_comment_like_serializer.errors,
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


"""This API will add like to post comment"""

class RemovePostCommentLikeAPIView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        add_post_comment_like_serializer = AddPostCommentLikeSerializer(
            data=request.data, context={"request": request}
        )

        if add_post_comment_like_serializer.is_valid():
            add_post_comment_like_serializer.delete()
            response = {
                "status_code": status.HTTP_204_NO_CONTENT,
                "message": "comment like removed",
            }
            return Response(response, status=status.HTTP_204_NO_CONTENT)

        response = {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": "bad request",
            "data": add_post_comment_like_serializer.data,
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


"""This API will show the user story highlights"""

class GetStoryHighlightsAPIView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = Talvidouser.objects.get(firebase_uid=request.user)
        story_highlights = user.story_hightlight_user.all()
        story_hightlights_serializer = GetStoryHighlightsModelSerializer(
            story_highlights, many=True, context={"request": request}
        )
        response = {
            "status_code": status.HTTP_200_OK,
            "message": "ok",
            "data": story_hightlights_serializer.data,
        }
        return Response(response, status=status.HTTP_200_OK)


"""This APi will show all the posts"""

class GetUserAllPosts(APIView, PageNumberPaginationView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    page_size = 15 
    def get(self, request):
        user = Talvidouser.objects.filter(is_active=True)
        posts = Post.objects.select_related().filter(
            user__in=user.values_list("firebase_uid", flat=True)
        ).order_by("-created_at")
        posts_paginated = self.paginate_queryset(posts, request, view=self)
        post_serializer = GetPostModelSerializer(
            posts_paginated, many=True, context={"request": request}
        )
        return self.get_paginated_response(post_serializer.data)
