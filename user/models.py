from django.db import models
from django.contrib.auth.models import User
from PIL import Image


# Create your models here.

# User Profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telephone = models.CharField("Telephone Number 1*", max_length=50)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self):
        super().save()

        img = Image.open(self.image.path)
        if img.height > 500 or img.width > 500:
            output_size = (500, 500)
            img.thumbnail(output_size)
            img.save(self.image.path)


# Address Model !
class Address(models.Model):
    user = models.OneToOneField(User, models.CASCADE)
    address = models.CharField(max_length=55, blank=True, null=True)
    city = models.CharField(max_length=55, blank=True, null=True)
    state = models.CharField(max_length=55, blank=True, null=True)
    zip = models.PositiveSmallIntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.address} Profile'
