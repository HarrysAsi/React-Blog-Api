from django.contrib.auth.models import User, Group, Permission
from rest_framework.serializers import ModelSerializer, CharField, Serializer, IntegerField
from django.core.exceptions import ValidationError
from django.db.models import Q
from rest_framework.authtoken.models import Token
from user.models import Profile, Address
from rest_framework_jwt.settings import api_settings

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

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user.first())
        token = jwt_encode_handler(payload)
        token_object = Token.objects.filter(user_id=user_obj.id).first()

        # if token_object:
        #         #     print("Exists")
        #         #     Token.objects.update(user_id=user_obj.id, key=token)
        #         # else:
        #         #     print("Doesn'; exists")
        #         #     Token.objects.create(user_id=user_obj.id, key=token)

        data["token"] = token
        data['id'] = user_obj.id
        return data


"""
    USER SIGN UP ENDPOINT "...user/signup/"
    
    required: username, password, email  - optional first_name, last_name
    returns id, username, email, first_name, last_name
"""


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
        username = validated_data.get("username", None)
        email = validated_data.get("email", None)
        password = validated_data.get("password", None)
        first_name = validated_data.get('first_name', None)
        last_name = validated_data.get('last_name', None)

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


"""
    USER UPDATE PROFILE AND ADDRESS ENDPOINT "...user/update_profile/"
    
    required: id
    optional: tel, address, city, state, zip, token
    returns id, username, json web token (JWT)
"""


class UserUpdateProfileAddressSerializer(Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    # attributes required to endpoint
    id = IntegerField()
    telephone_number = CharField(allow_null=True, allow_blank=True)
    address = CharField(allow_null=True, allow_blank=True, max_length=50)
    city = CharField(allow_null=True, allow_blank=True, max_length=50)
    state = CharField(allow_null=True, allow_blank=True, max_length=50)
    zip = CharField(allow_null=True, max_length=5)
    token = CharField(read_only=True)

    def to_representation(self, instance):
        # print(instance)
        data = super(UserUpdateProfileAddressSerializer, self).to_representation(instance)
        # get the id for the profile
        # id = (list(data.items())[0])[1]
        # user_profile = Profile.objects.filter(user_id=id).values()
        # data["profile"] = user_profile
        # data["kappa"] = 'kappa'
        # response = {}
        # response["user"] = data
        return data
