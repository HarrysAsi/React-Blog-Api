from django.contrib.auth.models import User, Group, Permission
from rest_framework.serializers import ModelSerializer, CharField, Serializer
from django.core.exceptions import ValidationError
from django.db.models import Q
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

"""
    USER LOGIN ENDPOINT "...user/auth/"
    
    required: username, password
    returns id, username, json web token
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
    
    required: username, password, email
    returns id, username, json web token
"""


class UserCreateSerializer(ModelSerializer):
    class Meta:
        model = User

        fields = [
            'username',
            'email',
            'password',
        ]
        extra_kwargs = {"password":
                            {"write_only": True
                             },
                        }

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        username = validated_data["username"]
        email = validated_data["email"]
        password = validated_data["password"]
        user_object = User(
            username=username,
            email=email,
        )
        user_object.set_password(password)
        user_object.save()
        return user_object
