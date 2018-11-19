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


class Follower(models.Model):
    user = models.ForeignKey(User, models.CASCADE, related_name='user_id')
    follower = models.ForeignKey(User, models.CASCADE, related_name='follower_id')
    description = models.TextField(max_length=250, blank=True, null=True)

    class Meta:
        unique_together = (('user', 'follower'),)


class PostComment(models.Model):
    comment = models.CharField(max_length=500)
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_date = models.DateTimeField(auto_now=True)


class PostLike(models.Model):
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_date = models.DateTimeField(auto_now=True)


class Post(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    description = models.CharField(max_length=500)
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_date = models.DateTimeField(auto_now=True)
    comments = models.ManyToManyField(PostComment)
    likes = models.ManyToManyField(PostLike)
