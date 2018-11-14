from django.contrib import admin
from django.urls import path, include
from user.views import UserLoginApi, UserCreateApi, UserUpdateProfileAddressApi

urlpatterns = [
    path('auth/', UserLoginApi.as_view(), name='login'),
    path('signup/', UserCreateApi.as_view(), name='signup'),
    path('update_profile/', UserUpdateProfileAddressApi.as_view(), name='update_profile'),
]
