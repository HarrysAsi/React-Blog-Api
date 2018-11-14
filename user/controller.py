from user.models import Profile, Address


def update_profile(data):
    try:
        profile = Profile.objects.get_or_create(user_id=data["id"])[0]
        profile.telephone = data.get("telephone_number", None)
        profile.save()
        return True
    except:
        return False


def update_address(data):
    try:
        address = Address.objects.get_or_create(user_id=data["id"])[0]
        address.address = data.get("address", None)
        address.state = data.get("state", None)
        address.city = data.get("city", None)
        address.zip = data.get("zip", None)
        address.save()
        return True
    except:
        return False
