from django.db import models
from django.contrib.auth.models import User


# User Profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telephone = models.CharField("Telephone Number 1*", max_length=50)
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_date = models.DateTimeField(auto_now=True)


# Address Model !
class Address(models.Model):
    user = models.OneToOneField(User, models.CASCADE)
    address = models.CharField(max_length=55, blank=True, null=True)
    city = models.CharField(max_length=55, blank=True, null=True)
    state = models.CharField(max_length=55, blank=True, null=True)
    zip = models.PositiveSmallIntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.address} Profile'
