from django.contrib.auth.models import User, Group, Permission
from rest_framework.serializers import ModelSerializer, CharField
from django.core.exceptions import ValidationError
from django.db.models import Q
from rest_framework.authtoken.models import Token

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
        print(user_obj)
        print(data)
        return data