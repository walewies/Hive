from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView, DetailView
from .models import Post, Comment
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from datetime import datetime

from django.http import JsonResponse

from accounts.models import User

# Create your views here.
class CreatePost(CreateView):
    model = Post
    fields = ('meme_file', 'description')
    template_name = "CreatePost.html"

    def get_success_url(self):
        return reverse_lazy("accounts:profile", kwargs={"slug": self.request.user.slug})

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.memer = self.request.user
        obj.datetime_posted = datetime.now()
        obj.save()
        return HttpResponseRedirect(self.get_success_url())

class PostAndCommentsView(TemplateView):
    template_name = "PostView.html"

    def post(self, request, pk):

        # Like/Unlike post on request.
        if request.POST.get("task") == "like":

            user = self.request.user.slug
            post_pk = request.POST.get("post_pk")
            current_post = Post.objects.get(pk=int(post_pk))

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

            user = self.request.user.slug
            post_pk = request.POST.get("post_pk")
            current_post = Post.objects.get(pk=int(post_pk))
            
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

        else:
            comment_body = request.POST.get('comment_body')
            comment = Comment.objects.create(memer=self.request.user, body=comment_body, post=Post.objects.get(id=pk))

            return JsonResponse({
                "comment_body": comment.body, 
                "comment_memer": comment.memer.username,
                "comment_memer_slug": comment.memer.slug
            }, status=200)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post_user"] = Post.objects.get(id=self.kwargs['pk']).memer
        context["current_user"] = self.request.user
        context["post"] = Post.objects.get(id=self.kwargs['pk'])
        context["comments"] = Comment.objects.filter(post=self.kwargs['pk'])
        context["followers"] = context["post_user"].followers.split(",")
        context["likes"] = context["post"].likes.split(",")
        return context
        
    def get_success_url(self, **kwargs):
        return reverse_lazy("posts:view_post", kwargs={"pk": self.kwargs['pk']})