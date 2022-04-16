from django.shortcuts import render
from django.views.generic import TemplateView
from posts.models import Post
from accounts.models import User

from django.http import JsonResponse

# Create your views here.
class HomePageView(TemplateView):
    template_name = "home.html"

    def post(self, request):
        user = self.request.user.slug
        user_model = User.objects.filter(slug=user)
        list_user_interests = user_model[0].interests.split(",")
        if list_user_interests[0] == "":
            list_user_interests.pop(0) # removes initial empty string
        print(list_user_interests)
        dict_user_interests = {}

        if len(list_user_interests) > 0:
            for i in range(0, len(list_user_interests), 2):
                dict_user_interests[list_user_interests[i].lower()] = int(list_user_interests[i+1])

        post_pk = request.POST.get("post_pk")
        current_post = Post.objects.get(pk=int(post_pk))
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        context["posts"] = Post.objects.all()
        return context