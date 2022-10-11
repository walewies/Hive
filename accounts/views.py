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
from posts.models import Post
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

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet
        context['user_profile'] = User.objects.get(slug=self.kwargs['slug'])
        context['followers_amount'] = context['user_profile'].followers_amount
        context['following_amount'] = context['user_profile'].following_amount
        context['user_current'] = self.request.user
        context['posts'] = Post.objects.filter(memer=context['user_profile'].id)
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