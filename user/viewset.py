from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
from django.contrib.auth.models import User, Group
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView
from user.controller import update_profile, update_address
from rest_framework.permissions import AllowAny, IsAuthenticated
from user.models import Post, PostLike, PostComment, Follower
from user.pagination import PostCommentsPagination

from user.serializers import UserLoginSerializer, UserCreateSerializer, UserUpdateProfileAddressSerializer, \
    UserRetrieveProfileAddressSerializer, PostSerializer, FollowerSerializer, FollowerPostsSerializer, \
    CommentsSerializer


class FollowerPostsApi(ListAPIView):
    """
    API endpoint which returns all the posts for the followers
   """
    serializer_class = FollowerPostsSerializer
    permission_classes = [AllowAny]

    # pagination_class = PostCommentsPagination

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        user_id = self.kwargs['pk']
        print(user_id)
        followers = Follower.objects.filter(user=user_id)
        print(followers)
        follower_ids = []
        for entry in followers:
            # print(entry.follower_id)
            follower_ids.append(entry.follower_id)
        # print(follower_ids)
        return Post.objects.filter(user__in=follower_ids)


class FollowerListApi(ListAPIView):
    """
    API endpoint which returns all the post for a user
    """
    serializer_class = FollowerSerializer
    permission_classes = [AllowAny]
    queryset = Follower.objects.all()

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        user_id = self.kwargs['pk']
        print(user_id)
        return Follower.objects.filter(user=user_id)


class PostListApi(ListAPIView):
    """
    API endpoint which returns all the post for a user
    """
    serializer_class = PostSerializer
    permission_classes = [AllowAny]
    queryset = Post.objects.all()

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        user_id = self.kwargs['pk']
        print(user_id)
        return Post.objects.filter(user=user_id)


class PostCreateApi(CreateAPIView):
    """
    API endpoint that creates a post for a specific user
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny]


class UserCreateApi(CreateAPIView):
    """
    API endpoint that creates a requested user
    """
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]


class UserLoginApi(APIView):
    """
    API endpoint for user authentication. Also returns the JWT (Json web token)
    """
    queryset = User.objects.all()
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            print(new_data)
            return Response(new_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class UserRetrieveProfileAddressApi(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserRetrieveProfileAddressSerializer
    permission_classes = [AllowAny]


class UserUpdateProfileAddressApi(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateProfileAddressSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserUpdateProfileAddressSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            data = serializer.data
            try:
                address = update_address(data)
                profile = update_profile(data)
                print(address)
                print(profile)
            except:
                return Response({"error":
                                     {"error_code": HTTP_500_INTERNAL_SERVER_ERROR}},
                                status=HTTP_500_INTERNAL_SERVER_ERROR)
            if address is False or profile is False:
                return Response({"error":
                                     {"error_code": HTTP_400_BAD_REQUEST, "status": serializer.errors}},
                                status=HTTP_400_BAD_REQUEST)
            else:
                return Response({"success":
                                     {"data": data}}, status=HTTP_200_OK)

        return Response({"error":
                             {"error_code": HTTP_400_BAD_REQUEST, "status": serializer.errors}},
                        status=HTTP_400_BAD_REQUEST)
