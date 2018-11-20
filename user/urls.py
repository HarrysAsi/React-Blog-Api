from django.contrib import admin
from django.urls import path, include
from user.viewset import UserLoginApi, UserCreateApi, UserUpdateProfileAddressApi, UserRetrieveProfileAddressApi, \
    PostCreateApi, PostListApi, FollowerListApi, FollowerPostsApi, PostCommentCreateApi

urlpatterns = [
    path('auth/', UserLoginApi.as_view(), name='login'),
    path('signup/', UserCreateApi.as_view(), name='signup'),
    path('update_profile/', UserUpdateProfileAddressApi.as_view(), name='update_profile'),
    path('retrieve_profile/<int:pk>', UserRetrieveProfileAddressApi.as_view(), name='retrieve_profile'),
    path('create_post/', PostCreateApi.as_view(), name='create_post'),
    path('retrieve_posts/<int:pk>', PostListApi.as_view(), name='retrieve_posts'),
    path('follows/<int:pk>', FollowerListApi.as_view(), name='follows'),
    path('follower_posts/<int:pk>', FollowerPostsApi.as_view(), name='follows'),
    path('comment/<int:pk>', PostCommentCreateApi.as_view(), name='comment'),
    # path('create_comment/<int:pk>', PostCommentApi.as_view(), name='create_comment'),
]
