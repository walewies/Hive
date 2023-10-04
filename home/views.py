from django.shortcuts import render
from django.views.generic import TemplateView
from posts.models import Post, Comment, Save, PostLike, PostDislike
from accounts.models import User, Follow

from django.http import JsonResponse

import random 
from datetime import datetime, timedelta
import pytz

# Create your views here.
class HomePageView(TemplateView):
    template_name = "home.html"

    def post(self, request):
        user = self.request.user.slug
        post_pk = request.POST.get("post_pk")
        current_post = Post.objects.get(pk=int(post_pk))

        # Like/Unlike post on request.
        if request.POST.get("task") == "like":
            user_model = User.objects.filter(slug=user) # .get() does not allow .update() on object
            order = ""

            # Unlike
            if PostLike.objects.filter(post=current_post, user=self.request.user):
                liked_post = PostLike.objects.get(post=current_post, user=self.request.user)
                liked_post.delete()
                order = "like"
            # Like
            else:
                # Check if post has been disliked by user and deletes dislike
                if PostDislike.objects.filter(post=current_post, user=self.request.user):
                    disliked_post = PostDislike.objects.get(post=current_post, user=self.request.user)
                    disliked_post.delete()

                PostLike.objects.create(post=current_post, user=self.request.user)
                order = "unlike"

            update_post = Post.objects.filter(pk=post_pk)
            current_likes_amount = len(PostLike.objects.filter(post=current_post))
            current_dislikes_amount = len(PostDislike.objects.filter(post=current_post))
            update_post.update(likes_amount=current_likes_amount, dislikes_amount=current_dislikes_amount)

            return JsonResponse({
                "order": order,
                "likes_amount":  current_likes_amount,
                "dislikes_amount": current_dislikes_amount
            }, status=200)

        # Dislike/Undislike post on request.
        if request.POST.get("task") == "dislike":
            user_model = User.objects.filter(slug=user) # .get() does not allow .update() on object

            order = ""

            # Undislike
            if PostDislike.objects.filter(post=current_post, user=self.request.user):
                dislike_object = PostDislike.objects.get(post=current_post, user=self.request.user)
                dislike_object.delete()
                order = "dislike"
            # Dislike
            else:
                # Check if post has been liked by user and deletes like
                if PostLike.objects.filter(post=current_post, user=self.request.user):
                    like_object = PostLike.objects.get(post=current_post, user=self.request.user)
                    like_object.delete()
                
                PostDislike.objects.create(post=current_post, user=self.request.user)
                order = "undislike"

            update_post = Post.objects.filter(pk=post_pk)
            current_dislikes_amount = len(PostDislike.objects.filter(post=current_post))
            current_likes_amount = len(PostLike.objects.filter(post=current_post))
            update_post.update(dislikes_amount=current_dislikes_amount, likes_amount= current_likes_amount)

            return JsonResponse({
                "order": order,
                "dislikes_amount":  current_dislikes_amount,
                "likes_amount": current_likes_amount
            }, status=200)

        # Follow/Unfollow Post-User on request.
        elif request.POST.get("task") == "follow":
            post_user = current_post.user
            current_user = self.request.user
            post_user_model = User.objects.filter(slug=current_post.user.slug)
            current_user_model = User.objects.filter(slug=self.request.user.slug)

            # Unfollow
            if Follow.objects.filter(follower=current_user, following=post_user):
                followship = Follow.objects.get(follower=current_user, following=post_user)
                followship.delete()
                order = "follow"

            # Follow
            else:
                Follow.objects.create(follower=current_user, following=post_user)
                order = "unfollow"

            post_user_followers = len(Follow.objects.filter(following=post_user))
            current_user_following =  len(Follow.objects.filter(follower=current_user))

            post_user_model.update(followers_amount=post_user_followers)
            current_user_model.update(following_amount=current_user_following)

            return JsonResponse({
                "order": order,
                "post_user": current_post.user.slug # To change all posts regarding following.
            }, status=200)
        
        # Save/Unsave post on command.
        elif request.POST.get("task") == "save":
            # Unsave
            if Save.objects.filter(post=current_post, user=self.request.user):
                unsaved_post = Save.objects.get(post=current_post, user=self.request.user)
                unsaved_post.delete()
                order = "save"
            # Save
            else:
                Save.objects.create(post=current_post, user=self.request.user)
                order = "unsave"

            return JsonResponse({
                "order": order
            }, status=200)
            

    def get_context_data(self, **kwargs):
        posts_num = 100
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user

        context['posts'] = random.sample(list(Post.objects.all()), k=len(Post.objects.all()))

        if not self.request.user.is_authenticated:
            return context

        # Makes list of all the accounts the current user follows.
        following_queryset = Follow.objects.filter(follower=self.request.user)
        context["following"] = []
        for following in following_queryset:
            context["following"].append(following.following)

        # Makes a list of all the liked posts of user.
        likes_queryset = PostLike.objects.filter(user=self.request.user)
        context["likes"] = []
        for like in likes_queryset:
            context["likes"].append(like.post)

        # Makes a list of all the disliked posts of user.
        dislikes_queryset = PostDislike.objects.filter(user=self.request.user)
        context["dislikes"] = []
        for dislike in dislikes_queryset:
            context["dislikes"].append(dislike.post)

        # Makes a list of all the saved posts of the current user.
        saves_queryset = Save.objects.filter(user=self.request.user)
        context["saved_posts"] = []
        for save in saves_queryset:
            context["saved_posts"].append(save.post)
            
        return context