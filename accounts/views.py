from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, TemplateView, ListView, UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect, JsonResponse
from django.utils.text import slugify
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect
from .models import User, Follow
from posts.models import Post, PostLike, PostDislike, Save
from . import forms

# Create your views here.
class SignUp(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy("accounts:login")
    template_name = "signup.html"

class MyLoginView(LoginView):
    template_name="login.html"

class ProfileView(TemplateView):
    template_name = "UserProfile.html"

    def post(self, request, slug):
        user = slug
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
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

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

        # User's personal data
        context['user_profile'] = User.objects.get(slug=self.kwargs['slug'])
        context['followers_amount'] = context['user_profile'].followers_amount
        context['following_amount'] = context['user_profile'].following_amount
        context['user_current'] = self.request.user
        context['posts'] = Post.objects.filter(user=context['user_profile'].id)
        context['posts_amount'] = len(context['posts'])
        return context

class EditProfileView(UpdateView):
    model = get_user_model()
    template_name = "EditUserProfile.html"
    fields = ("username", "profile_pic", "email")

    def get_success_url(self):
        return reverse_lazy("accounts:profile", kwargs={"slug": self.request.user.slug })

class ChangeUserPassword(TemplateView):
    template_name = "ChangeUserPassword.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context

def ValidateUserPassword(request, slug):
    UserObj = User.objects.get(username=request.user.username)
    # print(request.POST.get("old_password"))
    # print(make_password(request.POST.get("old_password")))
    # print(UserObj.password)
    if check_password(request.POST.get("old_password"), UserObj.password):
        if request.POST.get("new_password1") == request.POST.get("new_password2"):
            UserObj.set_password(request.POST.get("new_password1"))
            UserObj.save()
            return redirect("accounts:password_change_success", slug=request.user.slug)
        else:
            return render(request, "ChangeUserPassword.html", {"non_matching_passwords": True, "incorrect_password": False})
    else:
        return render(request, "ChangeUserPassword.html", {"incorrect_password": True, "non_matching_passwords": False})


class PasswordChangeSuccess(TemplateView):
    template_name = "PasswordChangeSuccess.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context

class UserFollowing(TemplateView):
    template_name = "UserFollowing.html"

    def post(self, request, slug):
        follow_user = User.objects.get(slug=request.POST.get("follow_user"))
        current_user = self.request.user
        follow_user_model = User.objects.filter(slug=follow_user.slug)
        current_user_model = User.objects.filter(slug=current_user.slug)

        # Follow/Unfollow
        if request.POST.get("task") == "follow":

            # Unfollow
            if Follow.objects.filter(following=follow_user, follower=self.request.user):
                follow_obj = Follow.objects.get(following=follow_user, follower=self.request.user)
                follow_obj.delete()
                order = "follow"
            # Follow
            else:
                Follow.objects.create(following=follow_user, follower=self.request.user)
                order = "unfollow"

            follow_user_followers = len(Follow.objects.filter(following=follow_user))
            current_user_following =  len(Follow.objects.filter(follower=current_user))

            follow_user_model.update(followers_amount=follow_user_followers)
            current_user_model.update(following_amount=current_user_following)

            return JsonResponse({
                "order": order,
            }, status=200)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["current_user"] = self.request.user
        context["profile_user"] = User.objects.get(slug=kwargs["slug"])
        context["following"] = Follow.objects.filter(follower=self.request.user)

        return context

class UserFollowers(TemplateView):
    template_name = "UserFollowers.html"

    def post(self, request, slug):
        follow_user = User.objects.get(slug=request.POST.get("follow_user"))
        current_user = self.request.user
        follow_user_model = User.objects.filter(slug=follow_user.slug)
        current_user_model = User.objects.filter(slug=current_user.slug)

        # Follow/Unfollow
        if request.POST.get("task") == "follow":

            # Unfollow
            if Follow.objects.filter(following=follow_user, follower=self.request.user):
                follow_obj = Follow.objects.get(following=follow_user, follower=self.request.user)
                follow_obj.delete()
                order = "follow"
            # Follow
            else:
                Follow.objects.create(following=follow_user, follower=self.request.user)
                order = "unfollow"

            follow_user_followers = len(Follow.objects.filter(following=follow_user))
            current_user_following =  len(Follow.objects.filter(follower=current_user))

            follow_user_model.update(followers_amount=follow_user_followers)
            current_user_model.update(following_amount=current_user_following)

            return JsonResponse({
                "order": order,
            }, status=200)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["current_user"] = self.request.user
        context["profile_user"] = User.objects.get(slug=kwargs["slug"])

        following_queryset = Follow.objects.filter(follower=self.request.user)
        context["following"] = []
        for follow in following_queryset:
            context["following"].append(follow.following)

        context["followers"] = Follow.objects.filter(following=self.request.user)

        return context