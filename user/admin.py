from django.contrib import admin
from user.models import Address, Profile, Follower, Post, PostComment, PostLike

# Register your models here.

admin.site.register(Address)
admin.site.register(Profile)
admin.site.register(Follower)
admin.site.register(Post)
admin.site.register(PostComment)
admin.site.register(PostLike)
