from django.db import models
from accounts.models import User

# Create your models here.
class Post(models.Model):
    memer = models.ForeignKey(User, on_delete=models.CASCADE)
    meme_file = models.FileField(upload_to="posts/")
    likes = []

    description = models.TextField(max_length=256)

    def __str__(self):
        return "Post " + str(self.pk) + " by " + self.memer.username

class Comment(models.Model):
    memer = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    comment = models.TextField(max_length=256)

    def __str__(self):
        return self.memer.username + "'s comment on " + str(self.id)