from django.contrib import admin
from django.urls import path, include
from user.views import UserLoginApi

urlpatterns = [
    path('auth/', UserLoginApi.as_view(), name='login'),
]
