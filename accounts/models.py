from django.db import models
from django.contrib import auth
from django.utils import timezone
from django.utils.text import slugify


# Create your models here.
class User(auth.models.AbstractUser):
    profile_pic = models.ImageField(upload_to="profiles/", default="profiles/default_profile.jpeg")
    slug = models.SlugField(max_length=256)

    interests = models.TextField(blank=True)

    followers_amount = models.PositiveIntegerField(default=0)
    following_amount = models.PositiveIntegerField(default=0)

    chats = models.TextField(blank=True)
    chats_amount = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):     
        self.slug = self.username
        super().save(*args, **kwargs)

    def __str__(self):
        return "@{}".format(self.username)

class Follow(models.Model):
    follower = models.ForeignKey(User, related_name="follower_name", on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name="following_name", on_delete=models.CASCADE)