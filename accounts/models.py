from django.db import models
from django.contrib import auth
from django.utils import timezone
from django.utils.text import slugify


# Create your models here.
class User(auth.models.AbstractUser, auth.models.PermissionsMixin):

    profile_pic = models.ImageField(upload_to="profiles/", default="profiles/default_profile.jpeg")
    slug = models.SlugField(max_length=256)

    interests = models.TextField(blank=True)

    def save(self, *args, **kwargs):     
        self.slug = self.username
        super().save(*args, **kwargs)

    def __str__(self):
        return "@{}".format(self.username)
