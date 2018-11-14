from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
from django.contrib.auth.models import User, Group
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView, ListAPIView, UpdateAPIView, DestroyAPIView, CreateAPIView
from user.controller import update_profile, update_address
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated

from user.serializers import UserLoginSerializer, UserCreateSerializer, UserUpdateProfileAddressSerializer, \
    UserRetrieveProfileAddressSerializer


class UserCreateApi(CreateAPIView):
    """
    API endpoint that creates a requested user
    """
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]


class UserLoginApi(APIView):
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
