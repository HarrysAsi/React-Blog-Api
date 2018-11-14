from django.contrib import admin
from django.urls import path, include
from user.viewset import UserLoginApi, UserCreateApi, UserUpdateProfileAddressApi, UserRetrieveProfileAddressApi

urlpatterns = [
    path('auth/', UserLoginApi.as_view(), name='login'),
    path('signup/', UserCreateApi.as_view(), name='signup'),
    path('update_profile/', UserUpdateProfileAddressApi.as_view(), name='update_profile'),
    path('retrieve_profile/<int:pk>', UserRetrieveProfileAddressApi.as_view(), name='retrieve_profile'),
]
