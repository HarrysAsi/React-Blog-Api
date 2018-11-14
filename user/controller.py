from user.models import Profile, Address


def update_profile(data):
    try:
        profile = Profile.objects.get_or_create(user_id=data["id"])
        profile[0].telephone = data.get("telephone_number", None)
        if profile[0].save():
            return True
        else:
            return False
    except:
        return False


def update_address(data):
    try:
        address = Address.objects.get_or_create(user_id=data["id"])
        address[0].address = data.get("telephone_number", None)["address"]
        address[0].state = data.get("telephone_number", None)["state"]
        address[0].city = data.get("telephone_number", None)["city"]
        address[0].zip = data.get("telephone_number", None)["zip"]
        if address[0].save():
            return True
        else:
            return False
    except:
        return False
