from django.db import models
from django.contrib import auth
from django.utils import timezone


# Create your models here.
class User(auth.models.AbstractUser, auth.models.PermissionsMixin):

    profile_pic = models.ImageField(null=True, blank=True)

    def __str__(self):
        return "@{}".format(self.username)
