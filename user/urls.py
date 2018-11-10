from django.contrib import admin
from django.urls import path, include
from user.views import UserLoginApi, UserCreateApi

urlpatterns = [
    path('auth/', UserLoginApi.as_view(), name='login'),
    path('signup/', UserCreateApi.as_view(), name='signup'),
]
