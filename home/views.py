from django.shortcuts import render
from django.views.generic import TemplateView
from posts.models import Post, Comment, Saved
from accounts.models import User

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
            user_model = User.objects.filter(slug=user)
            list_user_interests = user_model[0].interests.split(",")
            if list_user_interests[0] == "":
                list_user_interests.pop(0) # removes initial empty string
            dict_user_interests = {}

            if len(list_user_interests) > 0:
                for i in range(0, len(list_user_interests), 2):
                    dict_user_interests[list_user_interests[i].lower()] = int(list_user_interests[i+1])

            current_post_description = current_post.description.split(",")
            current_likes_list = current_post.likes.split(",")
            order = ""

            if user in current_likes_list: # Unlike post
                current_likes_list.remove(user)
                for element in current_post_description:
                    dict_user_interests[element.lower()] -= 1
                order = "like"
            else: # Like post
                current_likes_list.append(user)
                for element in current_post_description:
                    if element.lower() in dict_user_interests.keys():
                        dict_user_interests[element.lower()] += 1
                    else:
                        dict_user_interests[element.lower()] = 1
                order = "unlike"

            updated_user_interests = ""
            for key in dict_user_interests.keys():
                updated_user_interests += "," + key + "," + str(dict_user_interests[key])
            updated_user_interests = updated_user_interests[1:]

            user_model.update(interests=updated_user_interests)

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


        # Follow/Unfollow Post-User on request.
        elif request.POST.get("task") == "follow":
            post_user = current_post.memer.slug
            post_user_model = User.objects.filter(slug=current_post.memer.slug)
            current_user_model = User.objects.filter(slug=self.request.user.slug)

            # Accounts for possible initial empty string.
            if len(current_post.memer.followers) != 0:
                followers = current_post.memer.followers.split(",")
            else:
                followers = []

            # Accounts for possible initial empty string.
            if len(self.request.user.following) != 0:
                following = self.request.user.following.split(",")
            else:
                following = []

            string_following = ""
            string_followers = ""

            # Unfollow
            if user in followers:
                followers.remove(user)
                following.remove(post_user)
                order = "follow"

            # Follow
            else:
                followers.append(user)
                following.append(post_user)
                order = "unfollow"

            string_followers = ",".join(followers)
            string_following = ",".join(following)
            
            num_followers = len(followers)
            num_following = len(following)

            post_user_model.update(followers=string_followers)
            post_user_model.update(followers_amount=num_followers)

            current_user_model.update(following=string_following)
            current_user_model.update(following_amount=num_following)

            return JsonResponse({
                "order": order,
                "post_user": current_post.memer.slug # To change all posts regarding following.
            }, status=200)
        
        # Save/Unsave post on command.
        elif request.POST.get("task") == "save":
            # Unsave
            if Saved.objects.filter(post=current_post, memer=self.request.user):
                unsaved_post = Saved.objects.get(post=current_post, memer=self.request.user)
                unsaved_post.delete()
                order = "save"
            # Save
            else:
                Saved.objects.create(post=current_post, memer=self.request.user)
                order = "unsave"

            return JsonResponse({
                "order": order
            }, status=200)
            

    def get_context_data(self, **kwargs):
        posts_num = 100
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user

        if self.request.user.is_authenticated:
            list_user_interests = self.request.user.interests.split(",")
        else:
            context['posts'] = random.sample(list(Post.objects.all()), k=len(Post.objects.all()))
            return context
        
        if len(Post.objects.all()) < posts_num or len(list_user_interests) < 2:
            working_posts = []
            for post in Post.objects.all():
                working_posts.append(post)
            context["posts"] = random.sample(working_posts, k=len(working_posts))
        else:
            dict_user_interests = {}
            total_interests = 0
            interest_memes_num = round(posts_num * (7/10))
            random_memes_num = posts_num - interest_memes_num
            for i in range(0, len(list_user_interests), 2):
                dict_user_interests[list_user_interests[i]] = int(list_user_interests[i+1])     
                total_interests += int(list_user_interests[i+1])
            
            if total_interests == 0:
                working_posts = []
                for post in Post.objects.all():
                    working_posts.append(post)
                context["posts"] = random.sample(working_posts, k=len(working_posts))
                return context
            
            dict_interest_sets = {}
            for key in dict_user_interests.keys():
                post_pool = []
                all_matches = []
                all_matches_queryset = Post.objects.filter(description__icontains=key)
                for match in all_matches_queryset:
                    all_matches.append(match)
                for post in all_matches:
                    if post.datetime_posted > datetime.now(pytz.utc) - timedelta(days=7):
                        for i in range(post.likes_amount):
                            post_pool.append(post)
                    else:
                        post_pool.append(post)
                dict_interest_sets[key] = [post_pool, dict_user_interests[key]]
                
            working_posts = []
            for key in dict_interest_sets.keys():
                working_set = random.sample(dict_interest_sets[key][0], k=round(dict_interest_sets[key][1]/total_interests*interest_memes_num))
                for item in working_set:
                    working_posts.append(item)
            
            all_weekly_memes = []
            all_weekly_memes_queryset = Post.objects.filter(datetime_posted__gt=datetime.now() - timedelta(days=7))
            for meme in all_weekly_memes_queryset:
                all_weekly_memes.append(meme)
            random_weekly_memes = random.sample(all_weekly_memes, k=random_memes_num)
            for meme in random_weekly_memes:
                working_posts.append(meme)

            context["posts"] = random.sample(list(dict.fromkeys(working_posts)), len(list(dict.fromkeys(working_posts)))) # removes duplicate items and shuffles.


        # Makes list of comments amounts by post.
        comments_by_post = {}
        for post in context["posts"]:
            comments_by_post[post] = len(Comment.objects.filter(post=post))

        context["comments_by_post"] = comments_by_post

        # Makes a list of all the saved posts of the current user.
        saved_posts_raw = Saved.objects.filter(memer=self.request.user)
        context["saved_posts"] = []
        for post in saved_posts_raw:
            context["saved_posts"].append(post.post)
            
        return context