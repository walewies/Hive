from django.db import models
from accounts.models import User

from datetime import datetime
import pytz

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    post_body = models.CharField(max_length=256, default="")
    post_file = models.FileField(upload_to="posts/", blank=True)

    likes_amount = models.IntegerField(default=0)
    dislikes_amount = models.IntegerField(default=0)

    comments_amount = models.IntegerField(default=0)

    datetime_posted = models.DateTimeField(default=datetime(2022, 4, 14, 20, 8, 7, 127325, tzinfo=pytz.UTC))

    def __str__(self):
        return "Post " + str(self.pk) + " by " + self.user.username

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    body = models.TextField(max_length=256)

    likes_amount = models.IntegerField(default=0)
    dislikes_amount = models.IntegerField(default=0)

    def __str__(self):
        return "Comment " + str(self.pk) + " by " + self.user.username + " on post " + str(self.post.pk)

class Subcomment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

    body = models.TextField(max_length=256)

    likes_amount = models.IntegerField(default=0)
    dislikes_amount = models.IntegerField(default=0)

    def __str__(self):
        return "Comment " + str(self.pk) + " by " + self.user.username + " on comment " + str(self.comment.pk)

class PostLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return "Like " + str(self.pk) + " by " + self.user.username + " on post " + str(self.post.pk)

class PostDislike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return "Dislike " + str(self.pk) + " by " + self.user.username + " on post " + str(self.post.pk)

class CommentLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

    def __str__(self):
        return "Like " + str(self.pk) + " by " + self.user.username + " on comment " + str(self.comment.pk)

class CommentDislike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return "Dislike " + str(self.pk) + " by " + self.user.username + " on post " + str(self.post.pk)

class SubcommentLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subcomment = models.ForeignKey(Subcomment, on_delete=models.CASCADE)

    def __str__(self):
        return "Like " + str(self.pk) + " by " + self.user.username + " on subcomment " + str(self.subcomment.pk)
        
class SubcommentDislike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return "Dislike " + str(self.pk) + " by " + self.user.username + " on post " + str(self.post.pk)
        
class Save(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return "Post " + str(self.post.pk) + " saved by " + self.user.username