from django.contrib.auth.models import User, Group, Permission
from rest_framework.serializers import ModelSerializer, CharField, Serializer
from django.core.exceptions import ValidationError
from django.db.models import Q
from rest_framework.authtoken.models import Token
from user.models import Profile, Address
from django.core import serializers
from rest_framework.parsers import JSONParser
from rest_framework.decorators import parser_classes
from django.http import JsonResponse
from json import dumps
from django.http import HttpRequest, HttpResponse
import json

"""
    USER LOGIN ENDPOINT "...user/auth/"
    
    required: username, password
    returns id, username, json web token (JWT)
"""


class UserLoginSerializer(ModelSerializer):
    # attributes required to endpoint
    username = CharField()
    token = CharField(allow_blank=True, read_only=True)

    # data to return
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'token')
        extra_kwargs = {"password": {
            "write_only": True
        }}

    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)
        if not username and not password:
            raise ValidationError("A username and password is required to login!")

        user = User.objects.filter(
            Q(username=username)
        ).distinct()

        if user.exists() and user.count() == 1:
            user_obj = user.first()
        else:
            raise ValidationError("Wrong username or password, please try again!")

        if user_obj:
            if not user_obj.check_password(password):
                raise ValidationError("Wrong username or password, please try again!")
        jwt_token = Token.objects.get_or_create(user=user_obj)
        data["token"] = jwt_token[0]
        data['id'] = user_obj.id
        return data


"""
    USER SIGN UP ENDPOINT "...user/signup/"
    
    required: username, password, email  - optional first_name, last_name
    returns id, username, email, first_name, last_name
"""


# class UserProfileSerializer(ModelSerializer):
#     class Meta:
#         model = Profile
#         fields = ('id', 'telephone', 'image')
#

class UserCreateSerializer(ModelSerializer):
    class Meta:
        model = User

        fields = [
            'id',
            'username',
            'email',
            'password',
            'first_name',
            'last_name',
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        username = validated_data["username"]
        email = validated_data["email"]
        password = validated_data["password"]
        # checking the data which is not required if is there, otherwise fills the forms with an empty string
        if "first_name" in validated_data:
            first_name = validated_data['first_name']
        else:
            first_name = ''

        if "last_name" in validated_data:
            last_name = validated_data['last_name']
        else:
            last_name = ''

        user_object = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name
        )

        user_object.set_password(password)
        user_object.save()

        profile_object = Profile(
            user_id=user_object.id,
        )
        address_object = Address(
            user_id=user_object.id
        )

        profile_object.save()
        address_object.save()
        return user_object

    def to_representation(self, instance):
        print(instance)
        data = super(UserCreateSerializer, self).to_representation(instance)
        # response = {}
        # get the id for the profile
        # id = (list(data.items())[0])[1]
        # user_profile = Profile.objects.filter(user_id=id).values()
        # data["profile"] = user_profile
        # response["user"] = data
        return data
