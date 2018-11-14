from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token


urlpatterns = [
    path('admin/', admin.site.urls),
    #     api urls
    path('user/', include('user.urls'), name='project-api'),
    path('api-token-auth/', obtain_jwt_token),
    path('api-token-refresh/', refresh_jwt_token),
    path('api-token-verify/', verify_jwt_token),
]
