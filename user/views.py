from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR, \
    HTTP_502_BAD_GATEWAY
from django.contrib.auth.models import User, Group
from user.serializers import UserLoginSerializer, UserCreateSerializer, UserUpdateProfileAddressSerializer
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView, ListAPIView, UpdateAPIView, DestroyAPIView, CreateAPIView
from user.controller import update_profile, update_address
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes


@permission_classes((AllowAny,))
class UserCreateApi(CreateAPIView):
    """
    API endpoint that creates a requested user
    """
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


@permission_classes((AllowAny,))
class UserLoginApi(APIView):
    queryset = User.objects.all()
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            print(new_data)
            return Response(new_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class UserUpdateProfileAddressApi(APIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateProfileAddressSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserUpdateProfileAddressSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            data = serializer.data
            try:
                update_profile(data)
                update_address(data)
            except:
                return Response({"error":
                                     {"error_code": HTTP_500_INTERNAL_SERVER_ERROR}},
                                status=HTTP_500_INTERNAL_SERVER_ERROR)
            return Response({"success":
                                 {"data": data}}, status=HTTP_200_OK)

        return Response({"error":
                             {"error_code": HTTP_400_BAD_REQUEST, "status": serializer.errors}},
                        status=HTTP_400_BAD_REQUEST)

    #
    # def post(self, request, *args, **kwargs):
    #     data = request.data
    #     serializer = UserUpdateProfileAddressSerializer(data=data)
    #     if serializer.is_valid(raise_exception=True):
    #         new_data = serializer.data
    #         return Response(new_data, status=HTTP_200_OK)
    #     return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
