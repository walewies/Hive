from django.db import models
from accounts.models import User

from datetime import datetime
import pytz

# Create your models here.
class Post(models.Model):
    memer = models.ForeignKey(User, on_delete=models.CASCADE)
    meme_file = models.FileField(upload_to="posts/")
    likes = models.TextField(default="", blank=True)
    likes_amount = models.IntegerField(default=0)
    datetime_posted = models.DateTimeField(default=datetime(2022, 4, 14, 20, 8, 7, 127325, tzinfo=pytz.UTC))

    description = models.TextField(max_length=256)

    def __str__(self):
        return "Post " + str(self.pk) + " by " + self.memer.username

class Comment(models.Model):
    memer = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    body = models.TextField(max_length=256)

    def __str__(self):
        return "Comment " + str(self.pk) + " by " + self.memer.username + " on post " + str(self.post.pk)