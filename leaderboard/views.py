from django.shortcuts import render
from django.views.generic import TemplateView

from posts.models import Post

from django.http import JsonResponse

from datetime import timedelta, datetime

# Create your views here.

class BaseLeaderboard(TemplateView):

    def post(self, request):
        post_pk = request.POST.get("post_pk")
        user = self.request.user.slug
        current_post = Post.objects.get(pk=int(post_pk))
        current_likes_list = current_post.likes.split(",")
        order = ""

        if user in current_likes_list:
            current_likes_list.remove(user)
            order = "like"
        else:
            current_likes_list.append(user)
            order = "unlike"

        current_likes_string = ""
        current_likes_string += current_likes_list[0]
        for i in range(1, len(current_likes_list)):
            current_likes_string += ","
            current_likes_string += current_likes_list[i]
        current_likes_amount = len(current_likes_list)
        Post.objects.filter(pk=int(post_pk)).update(likes=current_likes_string)
        Post.objects.filter(pk=int(post_pk)).update(likes_amount=current_likes_amount-1)
        return JsonResponse({
            "order": order,
            "likes_amount":  current_likes_amount - 1 # -1 Accounts for empty string at index 0.
        }, status=200)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = self.posts
        working_posts = {}
        working_posts_keys = []
        leaderboard = []
        for post in posts:
            working_posts[post.likes_amount] = []
            working_posts_keys.append(post.likes_amount)
        for post in posts:
            working_posts[post.likes_amount].append(post)
        working_posts_keys.sort(reverse=True)
        if len(posts) < 100:
            for key in working_posts_keys:
                leaderboard.append(working_posts[key].pop())
        else:
            for i in range(100):
                leaderboard.append(working_posts[working_posts_keys[i]].pop())
        context["leaderboard"] = leaderboard
        return context

class DailyLeaderboard(BaseLeaderboard):
    template_name = "DailyLeaderboard.html"

    def __init__(self):
        self.posts = Post.objects.filter(datetime_posted__gt=datetime.now() - timedelta(days=1))

class WeeklyLeaderboard(BaseLeaderboard):
    template_name = "WeeklyLeaderboard.html"

    def __init__(self):
        self.posts = Post.objects.filter(datetime_posted__gt=datetime.now() - timedelta(days=7))

class MonthlyLeaderboard(BaseLeaderboard):
    template_name = "MonthlyLeaderboard.html"

    def __init__(self):
        self.posts = Post.objects.filter(datetime_posted__gt=datetime.now() - timedelta(days=31))

class YearlyLeaderboard(BaseLeaderboard):
    template_name = "YearlyLeaderboard.html"

    def __init__(self):
        self.posts = Post.objects.filter(datetime_posted__gt=datetime.now() - timedelta(days=365))

class AllTimeLeaderboard(BaseLeaderboard):
    template_name = "AllTimeLeaderboard.html"

    def __init__(self):
        self.posts = Post.objects.all()